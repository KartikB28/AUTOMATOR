const { spawn } = require('child_process');
const path = require('path');
const net = require('net');

class PythonBridge {
  constructor() {
    this.process = null;
    this.port = null;
  }

  async findFreePort() {
    return new Promise((resolve, reject) => {
      const server = net.createServer();
      server.unref();
      server.on('error', reject);
      server.listen(0, () => {
        const port = server.address().port;
        server.close(() => resolve(port));
      });
    });
  }

  async waitForReady(port, timeout = 30000) {
    const start = Date.now();
    while (Date.now() - start < timeout) {
      try {
        const response = await fetch(`http://localhost:${port}/api/system/health`);
        if (response.ok) return true;
      } catch (e) {
        await new Promise(r => setTimeout(r, 500));
      }
    }
    throw new Error('Python server did not start in time');
  }

  async start() {
    this.port = await this.findFreePort();
    const { app } = require('electron');
    const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

    const backendPath = isDev
      ? path.join(__dirname, '../backend')
      : path.join(process.resourcesPath, 'backend');

    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

    this.process = spawn(pythonCmd, [
      '-m', 'uvicorn',
      'main:app',
      '--host', '127.0.0.1',
      '--port', String(this.port),
      '--log-level', 'warning'
    ], {
      cwd: backendPath,
      env: {
        ...process.env,
        PYTHONPATH: backendPath,
        PORT: String(this.port),
        APP_DATA_PATH: app.getPath('userData')
      }
    });

    this.process.stdout.on('data', d => console.log('[Python]', d.toString()));
    this.process.stderr.on('data', d => console.error('[Python Error]', d.toString()));
    this.process.on('exit', code => console.log('[Python] exited with code', code));

    await this.waitForReady(this.port);
    return this.port;
  }

  async stop() {
    if (this.process) {
      this.process.kill('SIGTERM');
      await new Promise(r => setTimeout(r, 2000));
      if (this.process.exitCode === null) this.process.kill('SIGKILL');
    }
  }
}

module.exports = { PythonBridge };
