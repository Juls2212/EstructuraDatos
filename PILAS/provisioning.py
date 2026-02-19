class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from empty stack.")
        return self._items.pop()

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


class ProvisionError(Exception):
    pass


class Action:
    """
    An Action represents a provisioning step with:
    - execute(): do the step
    - rollback(): undo/compensate the step
    """
    def __init__(self, name):
        self.name = name
        self.executed = False

    def execute(self, context):
        raise NotImplementedError

    def rollback(self, context):
        raise NotImplementedError


class CreateDatabase(Action):
    def __init__(self, db_name):
        super().__init__(f"CreateDatabase({db_name})")
        self.db_name = db_name

    def execute(self, context):
        print(f"Executing: {self.name}")
        context["database"] = self.db_name
        self.executed = True

    def rollback(self, context):
        if self.executed:
            print(f"Rolling back: DeleteDatabase({self.db_name})")
            context.pop("database", None)


class CreateBucket(Action):
    def __init__(self, bucket_name):
        super().__init__(f"CreateBucket({bucket_name})")
        self.bucket_name = bucket_name

    def execute(self, context):
        print(f"Executing: {self.name}")
        context["bucket"] = self.bucket_name
        self.executed = True

    def rollback(self, context):
        if self.executed:
            print(f"Rolling back: DeleteBucket({self.bucket_name})")
            context.pop("bucket", None)


class ConfigureSecrets(Action):
    def __init__(self, secret_key):
        super().__init__(f"ConfigureSecrets({secret_key})")
        self.secret_key = secret_key

    def execute(self, context):
        print(f"Executing: {self.name}")
        context["secrets"] = {"key": self.secret_key}
        self.executed = True

    def rollback(self, context):
        if self.executed:
            print("Rolling back: RemoveSecrets()")
            context.pop("secrets", None)


class DeployService(Action):
    def __init__(self, service_name, fail=False):
        super().__init__(f"DeployService({service_name})")
        self.service_name = service_name
        self.fail = fail

    def execute(self, context):
        print(f"Executing: {self.name}")
        if self.fail:
            raise ProvisionError("Deployment failed due to misconfiguration.")
        context["service"] = self.service_name
        self.executed = True

    def rollback(self, context):
        if self.executed:
            print(f"Rolling back: RemoveService({self.service_name})")
            context.pop("service", None)


class ProvisioningOrchestrator:
    """
    Runs actions in order. If one fails, it rollbacks previously executed actions
    using a stack (LIFO).
    """
    def __init__(self):
        self._undo_stack = Stack()
        self.context = {}

    def run(self, actions):
        print("=== Provisioning started ===")
        try:
            for action in actions:
                action.execute(self.context)
                # Only push after a successful execution
                self._undo_stack.push(action)

            print("\n=== Provisioning completed successfully ===")
            return True

        except Exception as e:
            print(f"\n!!! ERROR: {e}")
            print("=== Starting rollback (LIFO) ===")
            self._rollback_all()
            print("=== Rollback finished ===")
            return False

    def _rollback_all(self):
        while not self._undo_stack.is_empty():
            action = self._undo_stack.pop()
            try:
                action.rollback(self.context)
            except Exception as rollback_error:
                # In real systems you would log this; we keep it simple.
                print(f"Rollback error on {action.name}: {rollback_error}")

    def summary(self):
        print("\n--- Final Context State ---")
        if not self.context:
            print("(empty) - no resources left provisioned")
        else:
            for k, v in self.context.items():
                print(f"{k}: {v}")


# ===== Example Usage =====
if __name__ == "__main__":
    orchestrator = ProvisioningOrchestrator()

    actions = [
        CreateDatabase("student_portal_db"),
        CreateBucket("student-portal-assets"),
        ConfigureSecrets("API_KEY_123"),
        DeployService("student-portal-service", fail=True)  # simulate failure
    ]

    orchestrator.run(actions)
    orchestrator.summary()