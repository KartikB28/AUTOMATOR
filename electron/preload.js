const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  getPythonPort: () => ipcRenderer.invoke('get-python-port'),
  getAppPath: () => ipcRenderer.invoke('get-app-path'),
  getMediaPath: () => ipcRenderer.invoke('get-media-path'),
  openExternalLink: (url) => ipcRenderer.invoke('open-external-link', url),
  showNotification: (title, body) => ipcRenderer.invoke('show-notification', { title, body }),
  onTrayAction: (callback) => ipcRenderer.on('tray-action', (event, action) => callback(action))
});
