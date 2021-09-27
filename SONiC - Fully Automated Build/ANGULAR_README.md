# Angular Frontend Setup

I did this on Windows. I started by installing NodeJS: https://nodejs.org/dist/v14.17.6/node-v14.17.6-x64.msi

```bash
npm install -g @angular/cli

# cd to your project's directory
ng add @angular/material
```

## Debugging

1. Go to the debugging tab in Visual Studio code, hit the down arrow next to launch program and click launch Chrome.
2. I used the following configuration:

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "type": "chrome",
            "request": "launch",
            "name": "Launch Chrome against localhost",
            "url": "http://localhost:4200",
            "webRoot": "c:\\Users\\grant\\Documents\\trafficshaper\\angular"
        }
    ]
}
```