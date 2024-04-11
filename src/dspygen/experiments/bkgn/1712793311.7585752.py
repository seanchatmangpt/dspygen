I'm glad to see your enthusiasm for creating a highly complex and elegant code solution for a challenging problem. Here's an example of how you might structure your solution and guidelines for the sections you should include in your response.

---

Example Io:
Let's say we have the following Scala code that demonstrates an actor-based system for handling failures and restarts:

```scala
import akka.actor._

case object Start
case object Stop
case object Restart

class Worker extends Actor {
  println("Worker started...")
  var count = 0
  def receive = {
    case Start => {
      println("Worker received Start message")
      count = count + 1
    }
    case Stop => {
      println("Worker received Stop message")
      context.stop(self)
    }
    case Restart => {
      println("Worker received Restart message... Restarting Worker")
      count = 0
      throw new Exception("Restarting now...")
    }
  }
}

class Supervisor(worker: ActorRef) extends Actor {
  def receive = {
    case Start => {
      println("Supervisor received Start message")
      worker ! Start
    }
    case Restart => {
      println("Supervisor received Restart message... Restarting Supervisor")
      worker ! PoisonPill
      context.stop(self)
    }
  }
}

class RootSupervisor(worker: ActorRef) extends Actor {
  var supervisor = context.actorOf(Props(classOf[Supervisor], worker))
  def receive = {
    case Start => {
      println("RootSupervisor received Start message")
      supervisor ! Start
    }
  }
}

object Main extends App {
  val system = ActorSystem("failure-restart-system")
  val rootSupervisor = system.actorOf(Props(classOf[RootSupervisor], system.actorOf(Props(classOf[Worker]))), name = "rootSupervisor")
  rootSupervisor ! Start
  Thread.sleep(5000)
  rootSupervisor ! Restart
  system.terminate()
}
```

Challenge Description:
Translate the given Scala code to a Python equivalent using the Denz actor library. Maintain the actor hierarchy and messaging structure from the original Scala code. Implement a worker actor, supervisor actor, and root supervisor actor in Python using the Denz actor library. Ensure that actors can communicate and handle messages as expected. Test your implementation by simulating failures and observing the restart behavior.

---

Here's an example of an Elite Code Solution for this problem. Keep in mind that while I am providing you with a starting point, the Denz library may have certain implementation details or features that differ slightly from the Scala example. This is a high-level example and it is up to you to research the Denz library and fill in the implementation details.

Elite Code Solution:

```python
import denz

class Worker(denz.Actor):
    def on_start(self):
        print("Worker started...")
        self.count = 0

    def on_message(self, msg):
        if msg == "Start":
            print("Worker received Start message")
            self.count += 1
        elif msg == "Stop":
            print("Worker received Stop message")
            self.stop()
        elif msg == "Restart":
            print("Worker received Restart message... Restarting Worker")
            self.count = 0
            raise Exception("Restarting now...")

class Supervisor(denz.Actor):
    def __init__(self, worker):
        self.worker = worker

    def on_message(self, msg):
        if msg == "Start":
            print("Supervisor received Start message")
            self.worker.send("Start")
        elif msg == "Restart":
            print("Supervisor received Restart message... Restarting Supervisor")
            self.worker.stop()
            self.stop()

class RootSupervisor(denz.Actor):
    def __init__(self, worker):
        self.supervisor = self.spawn(Supervisor, worker)

    def on_message(self, msg):
        if msg == "Start":
            print("RootSupervisor received Start message")
            self.supervisor.send("Start")

# In the following example, "main" creates the system, spawns the RootSupervisor, and sends the "Start" message
# Implement the actual code that uses the Denz library.
```

This example should guide you towards implementing the Worker, Supervisor, and RootSupervisor actors in Python using the Denz library. The example does not include the creation of the Denz actor system or the sending of a "Restart" message to test the failure handling. You will need to research the Denz library to fill in the outstanding implementation details. The provided example uses some of the Denz actor library's features but could use more. Once you have implemented the Denz equivalents of the Scala code, test your implementation by simulating failures and observing the restart behavior of the actors.