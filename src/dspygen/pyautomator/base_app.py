import subprocess
import logging
import os
import tempfile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BaseApp:
    def __init__(self, app_name: str, script_dir: str = None):
        self.app_name = app_name
        self.script_dir = script_dir or tempfile.gettempdir()

    def execute_jxa(self, script: str, save_to_file: bool = False):
        if save_to_file:
            script_path = self.save_script(script)
            logger.debug(f"Script saved to: {script_path}")
        else:
            script_path = None

        logger.debug(f"Executing JXA script:\n{script}")

        try:
            if script_path:
                result = subprocess.run(['osascript', '-l', 'JavaScript', script_path], check=True, capture_output=True,
                                        text=True)
            else:
                result = subprocess.run(['osascript', '-l', 'JavaScript', '-e', script], check=True,
                                        capture_output=True, text=True)

            logger.debug(f"Script result: {result.stdout}")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"JXA script failed: {e.stderr}")
            raise

    def save_script(self, script: str, filename: str = None) -> str:
        if not filename:
            filename = f"{self.app_name}_script_{int(datetime.now().timestamp())}.jxa"
        script_path = os.path.join(self.script_dir, filename)

        with open(script_path, 'w') as file:
            file.write(script)

        logger.debug(f"Script written to: {script_path}")
        return script_path

    def request_access(self, entity_type: str, save_to_file: bool = False):
        script = f"""
        const app = Application.currentApplication();
        app.includeStandardAdditions = true;
        app.requestAccessToEntityTypeCompletion("{entity_type}", (granted, error) => {{
            if (!granted) {{
                throw new Error('Access to {entity_type} denied.');
            }}
        }});
        """
        return self.execute_jxa(script, save_to_file=save_to_file)

    def activate_app(self, save_to_file: bool = False):
        script = f"""
        const app = Application("{self.app_name}");
        app.activate();
        """
        return self.execute_jxa(script, save_to_file=save_to_file)

    def get_app(self, save_to_file: bool = False):
        script = f"Application('{self.app_name}');"
        return self.execute_jxa(script, save_to_file=save_to_file)
