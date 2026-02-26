type Priority = "STAT" | "NORMAL";
type TestType = "HEMATOLOGY" | "PCR" | "CHEMISTRY";

class Sample {
  private history: string[] = [];

  constructor(
    private id: string,
    private patientId: string,
    private sampleType: string,
    private priority: Priority,
    private testType: TestType
  ) {
    this.addHistory("Sample created");
  }

  getId() { return this.id; }
  getPriority() { return this.priority; }
  getTestType() { return this.testType; }

  addHistory(message: string) {
    this.history.push(message);
  }

  getHistory() {
    return this.history;
  }
}

class Queue<T> {
  private items: T[] = [];

  enqueue(item: T) { this.items.push(item); }
  dequeue(): T | null { return this.items.shift() ?? null; }
  isEmpty(): boolean { return this.items.length === 0; }
}

class LabMachine {
  private queue = new Queue<Sample>();

  constructor(private name: string, private supportedTest: TestType) {}

  supports(test: TestType): boolean {
    return this.supportedTest === test;
  }

  addSample(sample: Sample) {
    sample.addHistory(`Queued in ${this.name}`);
    this.queue.enqueue(sample);
  }

  process(): Sample | null {
    const sample = this.queue.dequeue();
    if (sample) {
      sample.addHistory(`Processed by ${this.name}`);
    }
    return sample;
  }
}

class LabSystem {
  private intake = new Queue<Sample>();
  private machines: LabMachine[];
  private allSamples: Sample[] = [];

  constructor() {
    this.machines = [
      new LabMachine("Hematology Analyzer", "HEMATOLOGY"),
      new LabMachine("PCR Station", "PCR"),
      new LabMachine("Chemistry Analyzer", "CHEMISTRY")
    ];
  }

  receive(sample: Sample) {
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
          log(`Routed ${sample.getId()} to ${machine["name"]}`);
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

  findSample(id: string): Sample | null {
    return this.allSamples.find(s => s.getId() === id) ?? null;
  }
}

const lab = new LabSystem();

function log(message: string) {
  const logBox = document.getElementById("log")!;
  logBox.textContent += message + "\n";
}

document.getElementById("btnReceive")!.addEventListener("click", () => {
  const id = (document.getElementById("sampleId") as HTMLInputElement).value;
  const patient = (document.getElementById("patientId") as HTMLInputElement).value;
  const type = (document.getElementById("sampleType") as HTMLInputElement).value;
  const priority = (document.getElementById("priority") as HTMLSelectElement).value as Priority;
  const test = (document.getElementById("testType") as HTMLSelectElement).value as TestType;

  const sample = new Sample(id, patient, type, priority, test);
  lab.receive(sample);
});

document.getElementById("btnDistribute")!.addEventListener("click", () => {
  lab.distribute();
});

document.getElementById("btnStep")!.addEventListener("click", () => {
  lab.step();
});

document.getElementById("btnRunAll")!.addEventListener("click", () => {
  lab.processAll();
});

document.getElementById("btnTrace")!.addEventListener("click", () => {
  const id = (document.getElementById("traceId") as HTMLInputElement).value;
  const sample = lab.findSample(id);
  const traceBox = document.getElementById("trace")!;

  if (!sample) {
    traceBox.textContent = "Sample not found";
    return;
  }

  traceBox.textContent = sample.getHistory().join("\n");
});