#
# Developed by 10Pines SRL
# License:
# This work is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View,
# California, 94041, USA.
#
import unittest
from ElevatorController import ElevatorController

class ElevatorControllerObserver(object):
    def __init__(self, elevatorController):
        elevatorController.attach(self)

    def notify(self, *args):
        for msg in args:
            getattr(self, msg)()

    def notifyClosingDoor(self):
        self.shouldBeImplementedBySubclass()

    def notifyClosedDoor(self):
        self.shouldBeImplementedBySubclass()

    def notifyMovingCabin(self):
        self.shouldBeImplementedBySubclass()

    def notifyStoppedCabin(self):
        self.shouldBeImplementedBySubclass()

    def notifyOpeningDoor(self):
        self.shouldBeImplementedBySubclass()

    def shouldBeImplementedBySubclass(self):
        raise RuntimeError("Should be implemented by subclass")


class ElevatorControllerConsole(ElevatorControllerObserver):
    def __init__(self, elevatorController):
        super(ElevatorControllerConsole, self).__init__(elevatorController)
        self._lines = []

    def lines(self):
        return self._lines

    def notifyClosingDoor(self):
        self._lines.append('Puerta Cerrandose')

    def notifyClosedDoor(self):
        self._lines.append('Puerta Cerrada')

    def notifyMovingCabin(self):
        self._lines.append('Cabina Moviendose')

    def notifyStoppedCabin(self):
        self._lines.append('Cabina Detenida')

    def notifyOpeningDoor(self):
        self._lines.append('Puerta Abriendose')

class ElevatorControllerStatusView(ElevatorControllerObserver):
    def __init__(self, elevatorController):
        super(ElevatorControllerStatusView, self).__init__(elevatorController)
        self._cabinStateFieldModel = ''
        self._cabinDoorStateFieldModel = ''

    def cabinStateFieldModel(self):
        return self._cabinStateFieldModel

    def cabinDoorStateFieldModel(self):
        return self._cabinDoorStateFieldModel

    def notifyClosingDoor(self):
        self._cabinDoorStateFieldModel = 'Closing'

    def notifyClosedDoor(self):
        self._cabinDoorStateFieldModel = 'Closed'

    def notifyMovingCabin(self):
        self._cabinStateFieldModel = 'Moving'

    def notifyStoppedCabin(self):
        self._cabinStateFieldModel = 'Stopped'

    def notifyOpeningDoor(self):
        self._cabinDoorStateFieldModel = 'Opening'

class ElevatorControllerViewTest(unittest.TestCase):

    def test01ElevatorControllerConsoleTracksDoorClosingState(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)

        elevatorController.goUpPushedFromFloor(1)

        lines = elevatorControllerConsole.lines()

        self.assertEquals(1,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])

    def test02ElevatorControllerConsoleTracksCabinState(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()

        lines = elevatorControllerConsole.lines()

        self.assertEquals(3,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])
        self.assertEquals("Puerta Cerrada",lines[1])
        self.assertEquals("Cabina Moviendose",lines[2])

    def test03ElevatorControllerConsoleTracksCabinAndDoorStateChanges(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)

        lines = elevatorControllerConsole.lines()

        self.assertEquals(5,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])
        self.assertEquals("Puerta Cerrada",lines[1])
        self.assertEquals("Cabina Moviendose",lines[2])
        self.assertEquals("Cabina Detenida",lines[3])
        self.assertEquals("Puerta Abriendose",lines[4])

    def test04ElevatorControllerCanHaveMoreThanOneView(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)
        elevatorControllerStatusView = ElevatorControllerStatusView(elevatorController)

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)

        lines = elevatorControllerConsole.lines()

        self.assertEquals(5,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])
        self.assertEquals("Puerta Cerrada",lines[1])
        self.assertEquals("Cabina Moviendose",lines[2])
        self.assertEquals("Cabina Detenida",lines[3])
        self.assertEquals("Puerta Abriendose",lines[4])

        self.assertEquals("Stopped",elevatorControllerStatusView.cabinStateFieldModel())
        self.assertEquals("Opening",elevatorControllerStatusView.cabinDoorStateFieldModel())


if __name__ == '__main__':
    unittest.main()
