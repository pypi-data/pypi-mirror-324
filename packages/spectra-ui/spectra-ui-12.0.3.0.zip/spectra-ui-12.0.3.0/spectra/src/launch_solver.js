"use strict";

importScripts("spectra_solver.js");
//importScripts("spectra_solver_debug.js"); // for debugging

function SetOutput(dataname, data)
{
    self.postMessage({data: data, dataname: dataname});
}

Module.onRuntimeInitialized = () => {
    self.addEventListener("message", (msgobj) => {
        Module.spectra_solver(msgobj.data.serno, msgobj.data.data);
        self.postMessage({data: null, dataname: ""});
        self.close();
    });
    self.postMessage("ready");    
}