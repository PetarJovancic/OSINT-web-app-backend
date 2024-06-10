import logging
import docker
from fastapi import HTTPException


client = docker.from_env()

async def run_theharvester_scan(website: str) -> str:
    try:
        container = client.containers.create(
            image="theharvester:latest",
            entrypoint="/root/.local/bin/theHarvester",
            command=["-b", "rapiddns,otx", "-d", website],
        )
        container.start()
        logs = container.logs(stream=True)
        output = ""
        for log in logs:
            output += log.decode('utf-8')
        
        container.wait()
        container.remove()
        return output
    except Exception as e:
        logging.exception(f"Error running The Harvester scan: {e}")
        raise HTTPException(status_code=500, detail="Error running The Harvester scan")
    
async def run_amass_scan(website: str) -> str:
    import subprocess
    try:
        # container = client.containers.create(
        #     image="amass:latest",
        #     entrypoint="/bin/amass",
        #     command=["amass", "enum", "-d", website],
        # )
        container = client.containers.create(
            image="amass:latest",
            # entrypoint="/bin/amass",
            command=["intel", "-d", "owasp.org"],
        )
        container.start()
        logs = container.logs(stream=True)
        output = ""
        for log in logs:
            output += log.decode('utf-8')

        container.wait()
        container.remove()
        return output
    except Exception as e:
        logging.exception(f"Error running Amass scan: {e}")
        raise HTTPException(status_code=500, detail="Error running Amass scan")