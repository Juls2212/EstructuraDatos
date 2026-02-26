"use strict";
class Sample {
    constructor(id, patientId, sampleType, priority, testType) {
        this.id = id;
        this.patientId = patientId;
        this.sampleType = sampleType;
        this.priority = priority;
        this.testType = testType;
        this.history = [];
        this.addHistory("Sample created");
    }
    getId() { return this.id; }
    getPriority() { return this.priority; }
    getTestType() { return this.testType; }
    addHistory(message) { this.history.push(message); }
    getHistory() { return this.history; }
}
class Queue {
    constructor() { this.items = []; }
    enqueue(item) { this.items.push(item); }
    dequeue() { return this.items.shift() ?? null; }
    isEmpty() { return this.items.length === 0; }
}
class LabMachine {
    constructor(name, supportedTest) {
        this.name = name;
        this.supportedTest = supportedTest;
        this.queue = new Queue();
    }
    supports(test) { return this.supportedTest === test; }
    addSample(sample) {
        sample.addHistory(`Queued in ${this.name}`);
        this.queue.enqueue(sample);
    }
    process() {
        const sample = this.queue.dequeue();
        if (sample) {
            sample.addHistory(`Processed by ${this.name}`);
        }
        return sample;
    }
}
class LabSystem {
    constructor() {
        this.intake = new Queue();
        this.allSamples = [];
        this.machines = [
            new LabMachine("Hematology Analyzer", "HEMATOLOGY"),
            new LabMachine("PCR Station", "PCR"),
            new LabMachine("Chemistry Analyzer", "CHEMISTRY")
        ];
    }
    receive(sample) {
        this.intake.enqueue(sample);
        this.allSamples.push(sample);
        log(`Received ${sample.getId()}`);
    }
    distribute() {
        while (!this.intake.isEmpty()) {
            const sample = this.intake.dequeue();
            if (!sample) return;
            for (const machine of this.machines) {
                if (machine.supports(sample.getTestType())) {
                    machine.addSample(sample);
                    log(`Routed ${sample.getId()} to ${machine.name}`);
                }
            }
        }
    }
    step() {
        for (const machine of this.machines) {
            const result = machine.process();
            if (result) {
                log(`Processed ${result.getId()}`);
            }
        }
    }
    processAll() {
        for (let i = 0; i < 10; i++) {
            this.step();
        }
    }
    findSample(id) {
        return this.allSamples.find(s => s.getId() === id) ?? null;
    }
}
const lab = new LabSystem();
function log(message) {
    const logBox = document.getElementById("log");
    logBox.textContent += message + "\n";
}
document.getElementById("btnReceive").addEventListener("click", () => {
    const id = document.getElementById("sampleId").value;
    const patient = document.getElementById("patientId").value;
    const type = document.getElementById("sampleType").value;
    const priority = document.getElementById("priority").value;
    const test = document.getElementById("testType").value;
    const sample = new Sample(id, patient, type, priority, test);
    lab.receive(sample);
});
document.getElementById("btnDistribute").addEventListener("click", () => {
    lab.distribute();
});
document.getElementById("btnStep").addEventListener("click", () => {
    lab.step();
});
document.getElementById("btnRunAll").addEventListener("click", () => {
    lab.processAll();
});
document.getElementById("btnTrace").addEventListener("click", () => {
    const id = document.getElementById("traceId").value;
    const sample = lab.findSample(id);
    const traceBox = document.getElementById("trace");
    if (!sample) {
        traceBox.textContent = "Sample not found";
        return;
    }
    traceBox.textContent = sample.getHistory().join("\n");
});