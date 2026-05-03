const { app, BrowserWindow, ipcMain, Tray, Menu, shell, Notification, nativeImage } = require('electron');
const path = require('path');
const { PythonBridge } = require('./python-bridge');

let mainWindow = null;
let tray = null;
let pythonBridge = null;
let pythonPort = 8765;

const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

async function createWindow() {
  pythonBridge = new PythonBridge();
  try {
    pythonPort = await pythonBridge.start();
  } catch (err) {
    console.error('Failed to start Python backend:', err);
  }

  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 1024,
    minHeight: 680,
    backgroundColor: '#0a0a0a',
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
    autoHideMenuBar: process.platform !== 'darwin',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      additionalArguments: [`--python-port=${pythonPort}`]
    }
  });

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools({ mode: 'detach' });
  } else {
    mainWindow.loadFile(path.join(__dirname, '../frontend/dist/index.html'));
  }

  mainWindow.on('closed', () => { mainWindow = null; });
}

function createTrayIcon() {
  // Create a simple 16x16 transparent icon programmatically
  const size = 16;
  const buffer = Buffer.alloc(size * size * 4);
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const i = (y * size + x) * 4;
      // Lightning bolt-ish pattern
      const isBolt = (
        (x >= 7 && x <= 9 && y >= 2 && y <= 5) ||
        (x >= 5 && x <= 8 && y >= 5 && y <= 8) ||
        (x >= 6 && x <= 9 && y >= 8 && y <= 11) ||
        (x >= 4 && x <= 7 && y >= 11 && y <= 14)
      );
      buffer[i] = isBolt ? 0 : 0;       // R
      buffer[i + 1] = isBolt ? 255 : 0; // G
      buffer[i + 2] = isBolt ? 136 : 0; // B
      buffer[i + 3] = isBolt ? 255 : 0; // A
    }
  }
  return nativeImage.createFromBuffer(buffer, { width: size, height: size });
}

function createTray() {
  try {
    const icon = createTrayIcon();
    tray = new Tray(icon);
    tray.setToolTip('The Automator');

    const contextMenu = Menu.buildFromTemplate([
      { label: 'Open Automator', click: () => { if (mainWindow) mainWindow.show(); else createWindow(); } },
      { type: 'separator' },
      {
        label: 'Pause All Bots',
        click: async () => {
          try {
            await fetch(`http://localhost:${pythonPort}/api/bots/pause-all`, { method: 'POST' });
          } catch (e) { console.error(e); }
        }
      },
      {
        label: 'Resume All Bots',
        click: async () => {
          try {
            await fetch(`http://localhost:${pythonPort}/api/bots/resume-all`, { method: 'POST' });
          } catch (e) { console.error(e); }
        }
      },
      { type: 'separator' },
      { label: 'Quit', click: () => { app.quit(); } }
    ]);
    tray.setContextMenu(contextMenu);
    tray.on('double-click', () => { if (mainWindow) mainWindow.show(); });
  } catch (err) {
    console.error('Tray creation failed:', err);
  }
}

ipcMain.handle('get-python-port', () => pythonPort);
ipcMain.handle('get-app-path', () => app.getPath('userData'));
ipcMain.handle('get-media-path', () => path.join(app.getPath('userData'), 'media'));
ipcMain.handle('open-external-link', (event, url) => shell.openExternal(url));
ipcMain.handle('show-notification', (event, { title, body }) => {
  new Notification({ title, body }).show();
});

app.whenReady().then(async () => {
  await createWindow();
  createTray();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (mainWindow === null) createWindow();
});

app.on('before-quit', async () => {
  if (pythonBridge) await pythonBridge.stop();
});
