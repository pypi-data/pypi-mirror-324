from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Any
import yaml
import os
from fastapi import Request
import logging
import subprocess
import json
import copy

# 로그 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

_LOGGER = logging.getLogger(__name__)

app = FastAPI()

# Templates 설정
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)


class Dashboard(BaseModel):
    name: str
    template_id: str
    labels: List[str]
    template_type: str
    dashboards: List[Dict[str, Any]]


class RunSubprocessRequest(BaseModel):
    environment: str
    dashboard: Dashboard


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/environment-files")
async def list_environment_files():
    # 환경 파일 경로 설정
    env_dir = os.path.expanduser("~/.spaceone/environments")
    _LOGGER.info(f"Environment directory: {env_dir}")
    
    # 디렉토리 존재 여부 확인 및 생성
    if not os.path.exists(env_dir):
        os.makedirs(env_dir)
        _LOGGER.info(f"Created environment directory: {env_dir}")

    # .yml 확장자 파일 목록 가져오기
    try:
        files = [f[:-4] for f in os.listdir(env_dir) if f.endswith('.yml') or f.endswith('.yaml')]
        _LOGGER.info(f"Environment files: {files}")
    except FileNotFoundError:
        return {"error": "Environment directory not found"}
    
    return {"files": files}

@app.post("/run-create-template-by-subprocess")
async def run_create_template_by_subprocess(request: RunSubprocessRequest):
    try:
        _LOGGER.info(f"Running subprocess with environment: {request.environment}, dashboard: {request.dashboard}")
        
        # subprocess 실행
        result = subprocess.run(
            ['spacectl', 'config', 'environment', '-s', request.environment],
            capture_output=True,
            text=True
        )
        _LOGGER.info(f"Subprocess output: {result.stdout}")
        if result.stderr:
            _LOGGER.error(f"Subprocess error: {result.stderr}")
        
        result = subprocess.run(
            ['spacectl', 'exec', 'register', 'repository.DashboardTemplate', '-j', request.dashboard.model_dump_json()],
            capture_output=True,
            text=True
        )
        _LOGGER.info(f"Subprocess output: {result.stdout}")
        if result.stderr:
            _LOGGER.error(f"Subprocess error: {result.stderr}")
        
        return {"message": "Subprocess executed successfully", "output": result.stdout}
    except Exception as e:
        _LOGGER.error(f"Error executing subprocess: {str(e)}")
        return {"error": "Failed to execute subprocess"}

@app.get("/list-dashboard-templates-by-subprocess")
async def list_dashboard_templates_by_subprocess():
    try:
        _LOGGER.info("Listing dashboard templates using subprocess")
        
        # subprocess 실행
        result = subprocess.run(
            ['spacectl', 'list', 'repository.DashboardTemplate', '--minimal', '-o', 'json'],
            capture_output=True,
            text=True
        )
        
        if result.stderr:
            _LOGGER.error(f"Subprocess error: {result.stderr}")
            return {"error": "Failed to list dashboard templates", "details": result.stderr}
        
        if not result.stdout.strip():
            _LOGGER.error("Subprocess returned empty output")
            return {"error": "No output from subprocess"}
        
        try:
            result = result.stdout.split(">")
            result = result[-1]
            _LOGGER.info(f"Subprocess output: {result}")
            json_result = json.loads(result)
            _LOGGER.info(f"Subprocess output: {json_result}")
            return {"templates": json_result}
        except json.JSONDecodeError as e:
            _LOGGER.error(f"JSON decode error: {str(e)}")
            return {"error": "Failed to decode JSON", "details": str(e)}
    except Exception as e:
        _LOGGER.error(f"Error listing dashboard templates: {str(e)}")
        return {"error": "Failed to list dashboard templates"}

@app.get("/delete-dashboard-template")
async def delete_dashboard_template(template_id: str):
    try:
        result = subprocess.run(['spacectl', 'exec', 'deregister', 'repository.DashboardTemplate','-p', f'template_id={template_id}'], capture_output=True, text=True)
        return {"message": "Dashboard template deleted successfully", "output": result.stdout}
    except Exception as e:
        _LOGGER.error(f"Error deleting dashboard template: {str(e)}")
        return {"error": "Failed to delete dashboard template"}

@app.put("/update-dashboard-template")
async def update_dashboard_template(template_id: str, updates: Dict[str, Any]):
    try:
        command = ['spacectl', 'exec', 'get', 'repository.DashboardTemplate', '-p', f'template_id={template_id}', '-o', 'json']
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.stderr:
            _LOGGER.error(f"Subprocess error: {result.stderr}")
            return {"error": "Failed to list dashboard templates", "details": result.stderr}
        
        if not result.stdout.strip():
            _LOGGER.error("Subprocess returned empty output")
            return {"error": "No output from subprocess"}
        
        try:
            result = result.stdout.split(">")
            result = result[-1]
            # _LOGGER.info(f"Subprocess output: {result}")
            json_result = json.loads(result)
            # _LOGGER.info(f"Subprocess output: {json_result}")
        except json.JSONDecodeError as e:
            _LOGGER.error(f"JSON decode error: {str(e)}")
            return {"error": "Failed to decode JSON", "details": str(e)}
        
        # example
        # updates = {
        #     "data_key": {"cost": "data.Actual Cost"},
        #     "plugin_id": {"plugin-azure-cost-mgmt-cost-datasource": "plugin-azure-cost-datasource"}
        # }

        # change dashboards
        new_dashboards = update_dashboards(json_result, updates)
        
        update_params = {
            "template_id": template_id
        }

        if new_dashboards:
            update_params["dashboards"] = new_dashboards

        if "name" in updates:
            update_params["name"] = updates["name"]
        
        if "labels" in updates:
            update_params["labels"] = updates["labels"]
        
        _LOGGER.info(f"update_params: {update_params}")

        result = subprocess.run(
            ['spacectl', 'exec', 'update', 'repository.DashboardTemplate', '-j', json.dumps(update_params)],
            capture_output=True,
            text=True
        )
        _LOGGER.info(f"Subprocess output: {result.stdout}")
        if result.stderr:
            _LOGGER.error(f"Subprocess error: {result.stderr}")
            return {"error": "Failed to update dashboard template", "details": result.stderr}
        
        return {"message": "Dashboard template updated successfully", "output": update_params}
    
    except Exception as e:
        _LOGGER.error(f"Error updating dashboard template: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update dashboard template")

def update_dashboards(json_result, updates):
    new_dashboards = []
    for dashboard in json_result["dashboards"]:
        layouts = dashboard.get("layouts", [])
        for layout_index, layout in enumerate(layouts):
            widgets = layout.get("widgets", [])
            for widget_index, widget in enumerate(widgets):
                data_tables = widget.get("data_tables", [])
                for data_table_index, data_table in enumerate(data_tables):
                    options = data_table.get("options", {}).get("COST", {})
                    data_key = options.get("data_key")
                    plugin_id = options.get("plugin_id")
                    _LOGGER.info(f"data_key: {data_key}, plugin_id: {plugin_id}")

                    # Check and update data_key
                    if data_key:
                        if "data_key" in updates and data_key and data_key in updates["data_key"]:
                            if options.get("data_key") == data_key:
                                options["data_key"] = updates["data_key"][data_key]

                    # Check and update plugin_id
                    if plugin_id:
                        if "plugin_id" in updates and plugin_id in updates["plugin_id"]:
                            if options.get("plugin_id") == plugin_id:
                                options["plugin_id"] = updates["plugin_id"][plugin_id]

        new_dashboards.append(dashboard)
    
    return new_dashboards

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
