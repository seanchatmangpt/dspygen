import objc
from Foundation import NSObject

class EKObject(NSObject):
    def __init__(self):
        EventKit = objc.importFramework("EventKit")
        self.inst = EventKit.EKObject.alloc().init()

    def has_changes(self):
        return self.inst.hasChanges()

    def is_new(self):
        return self.inst.isNew()

    def refresh(self):
        self.inst.refresh()

    def reset(self):
        self.inst.reset()

    def rollback(self):
        self.inst.rollback()

def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()
    ek = EKObject()
    print(ek)


if __name__ == '__main__':
    main()

