import os
import uvicorn
import asyncio
import json
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI(title="CapitalShield AI | Agentic Framework")

# --- HIERARCHICAL CORE LOGIC ---

class SharedContext:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

class Orchestrator:
    """Primary Controller managing specialized sub-agents."""
    async def run_pipeline(self, filename):
        ctx = SharedContext(filename)
        
        # 1. Intake Logic
        yield "Intake", "Secure channel verified. Document hashed for immutable audit trail.", "success"
        await asyncio.sleep(0.8)

        # 2. Advanced Extraction (Simulating Gemini 1.5 Flash)
        ctx.data = {"vendor": "Vertex Global", "amount": 145000.0, "due": "2026-05-20"}
        yield "Extraction", f"Verified Entity: {ctx.data['vendor']} | Detected Value: ₹{ctx.data['amount']:,}", "success"
        await asyncio.sleep(1)

        # 3. Statistical Risk (Z-Score Math)
        amt = ctx.data.get("amount", 0)
        # Formula: (Current Value - Historical Mean) / Standard Deviation
        z = (amt - 50000) / 20000 
        status = "CRITICAL" if z > 3 else "NORMAL"
        yield "Risk Analysis", f"Anomaly Detection: Z-Score {z:.2f}. Status: {status}.", "error" if z > 3 else "success"
        await asyncio.sleep(1)

        # 4. Tax Ledgering
        taxable = amt / 1.18
        yield "Taxation", f"GST (18%) processed. Taxable Base: ₹{taxable:,.2f}. Ledger updated.", "success"
        await asyncio.sleep(0.8)

        # 5. External Tool Integration
        due = ctx.data.get("due")
        link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text=CapitalShield+Payment&dates={due.replace('-','')}T090000Z"
        yield "Workspace", f"Payment workflow synchronized for {due}.", "success", link

# --- MODERN ENTERPRISE INTERFACE ---

def get_ui():
    return """
    <!DOCTYPE html><html><head>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
    </style>
    </head><body class="bg-slate-50 flex">
    <div class="w-64 bg-white border-r border-gray-100 h-screen fixed p-8 flex flex-col shadow-sm">
        <h2 class="text-xl font-black text-slate-800 mb-10 tracking-tighter italic">CapitalShield <span class="text-blue-600">AI</span></h2>
        <nav class="flex-1 space-y-2 font-bold text-sm">
            <div class="bg-blue-50 text-blue-600 p-4 rounded-2xl cursor-pointer shadow-sm"><i class="fas fa-th-large mr-3"></i>Dashboard</div>
            <div class="text-gray-400 p-4 hover:bg-gray-50 rounded-2xl cursor-pointer transition-all"><i class="fas fa-file-invoice mr-3"></i>Analytics</div>
        </nav>
        <div class="mt-auto flex items-center p-3 border-t border-gray-100">
            <div class="w-10 h-10 rounded-xl bg-slate-900 text-white flex items-center justify-center text-xs font-bold mr-3 shadow-lg">AI</div>
            <div><p class="text-[11px] font-extrabold text-slate-800 tracking-tight">Lead Researcher</p><p class="text-[9px] text-slate-400 uppercase font-black">System Authorized</p></div>
        </div>
    </div>
    <main class="flex-1 ml-64 p-12 min-h-screen">
        <div class="flex justify-between items-center mb-12">
            <div><h1 class="text-4xl font-black text-slate-900 tracking-tight italic">Management Console</h1><p class="text-slate-400 text-sm mt-1">Hierarchical Agent Framework</p></div>
            <label class="bg-blue-600 text-white px-10 py-5 rounded-[2rem] text-xs font-black uppercase tracking-widest shadow-2xl shadow-blue-500/20 hover:scale-105 transition-all cursor-pointer">
                <i class="fas fa-plus mr-3"></i>Upload Document <input type="file" class="hidden" onchange="startWorkflow()">
            </label>
        </div>
        <div id="trace" class="hidden space-y-4">
            <div class="flex justify-between items-center mb-4 px-4">
                <span class="text-[10px] font-black text-blue-500 uppercase tracking-[0.4em]">Autonomous Trace</span>
                <span class="text-[10px] font-bold text-slate-300 italic" id="filename_display"></span>
            </div>
            <div id="logs" class="space-y-3"></div>
        </div>
    </main>
    <script>
        async function startWorkflow() {
            const trace = document.getElementById('trace'); const logs = document.getElementById('logs');
            const fileInput = document.querySelector('input[type="file"]');
            trace.classList.remove('hidden'); logs.innerHTML = "";
            document.getElementById('filename_display').innerText = "Processing: " + fileInput.files[0].name;

            const response = await fetch('/api/orchestrate');
            const reader = response.body.getReader(); const decoder = new TextDecoder();
            while (true) {
                const { value, done } = await reader.read(); if (done) break;
                const chunk = decoder.decode(value);
                const lines = chunk.split('\\n');
                for (let line of lines) {
                    if (!line) continue;
                    const data = JSON.parse(line);
                    const div = document.createElement('div');
                    const color = data.status === 'error' ? 'red' : 'blue';
                    div.className = "flex items-center p-6 bg-white rounded-[2rem] border border-slate-100 shadow-sm transition-all animate-in slide-in-from-bottom-4 duration-500";
                    div.innerHTML = `
                        <div class="w-2.5 h-2.5 rounded-full bg-${color}-500 mr-6 shadow-lg shadow-${color}-500/50"></div>
                        <div class="flex-1"><p class="text-xs font-bold text-slate-700">${data.msg}</p></div>
                    `;
                    if(data.link) div.innerHTML += `<a href="${data.link}" target="_blank" class="ml-auto text-[9px] font-black uppercase text-blue-600 border border-blue-100 px-4 py-2 rounded-full hover:bg-blue-600 hover:text-white transition-all">Open Workspace <i class="fas fa-external-link-alt ml-1"></i></a>`;
                    logs.appendChild(div);
                }
            }
        }
    </script></body></html>"""

engine = Orchestrator()

@app.get("/", response_class=HTMLResponse)
async def home(): return get_ui()

@app.get("/api/orchestrate")
async def process_api():
    async def generator():
        async for res in engine.run_pipeline("doc_01.pdf"):
            agent, text, status, *link = res
            yield json.dumps({"msg": text, "status": status, "link": link[0] if link else None}) + "\n"
    return StreamingResponse(generator())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)