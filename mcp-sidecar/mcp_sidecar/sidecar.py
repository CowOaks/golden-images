import ssl
import os
import subprocess
import logging
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-sidecar")

CERT_DIR = os.environ.get("CERT_DIR", "/certs")
CLIENT_CERT = os.path.join(CERT_DIR, "sidecar.crt")
CLIENT_KEY = os.path.join(CERT_DIR, "sidecar.key")
CA_CERT = os.path.join(CERT_DIR, "ca.crt")

MASTER_MCP_HOST = os.environ.get("MASTER_MCP_HOST", "192.168.1.35")
MASTER_MCP_PORT = int(os.environ.get("MASTER_MCP_PORT", "8443"))

APP_NAME = os.environ.get("APP_NAME", "unknown-app")
APP_LOG_PATH = os.environ.get("APP_LOG_PATH", "/app/logs/app.log")
APP_CONTAINER_NAME = os.environ.get("APP_CONTAINER_NAME", APP_NAME)


def load_mtls_context() -> ssl.SSLContext:
    if not (os.path.exists(CLIENT_CERT) and os.path.exists(CLIENT_KEY) and os.path.exists(CA_CERT)):
        raise FileNotFoundError(
            f"Missing certs in {CERT_DIR}. Expected sidecar.crt, sidecar.key, ca.crt"
        )
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile=CA_CERT)
    context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    context.verify_mode = ssl.CERT_REQUIRED
    logger.info("mTLS context loaded successfully for app=%s", APP_NAME)
    return context


ssl_context = load_mtls_context()

mcp = FastMCP(f"{APP_NAME}-sidecar")


@mcp.tool()
def read_logs(lines: int = 100) -> str:
    """Return the last N lines of this app's log file."""
    try:
        result = subprocess.run(
            ["tail", "-n", str(lines), APP_LOG_PATH],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout or "(no log output)"
    except Exception as e:
        logger.error("read_logs failed: %s", e)
        return f"error reading logs: {e}"


@mcp.tool()
def restart_container() -> str:
    """Restart the target app container (low-risk, auto-approvable action)."""
    try:
        result = subprocess.run(
            ["docker", "restart", APP_CONTAINER_NAME],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            logger.info("Restarted container %s", APP_CONTAINER_NAME)
            return f"restarted {APP_CONTAINER_NAME}"
        return f"restart failed: {result.stderr}"
    except Exception as e:
        logger.error("restart_container failed: %s", e)
        return f"error restarting container: {e}"


@mcp.tool()
def health_check() -> str:
    """Basic health probe this sidecar can report back to the master."""
    return f"{APP_NAME} sidecar alive, cert_dir={CERT_DIR}, master={MASTER_MCP_HOST}:{MASTER_MCP_PORT}"


if __name__ == "__main__":
    logger.info("Starting MCP sidecar for %s, connecting to master at %s:%s",
                APP_NAME, MASTER_MCP_HOST, MASTER_MCP_PORT)
    mcp.run()

