import pygame
import time

class XboxController:
    BUTTON_NAMES = {
        0: "A",
        1: "B",
        2: "X",
        3: "Y",
        4: "LB",
        5: "RB",
        6: "Back",
        7: "Start",
        8: "Xbox",
        9: "Left Stick",
        10: "Right Stick"
    }

    AXIS_NAMES = {
        0: "Left Stick X",
        1: "Left Stick Y",
        2: "Left Trigger",
        3: "Right Stick X",
        4: "Right Stick Y",
        5: "Right Trigger"
    }

    HAT_NAMES = {
        0: "D-pad"
    }

    def __init__(self, joystick_number=0):
        pygame.init()
        pygame.joystick.init()
        
        if pygame.joystick.get_count() == 0:
            raise Exception("No joystick connected")
        
        self.joystick = pygame.joystick.Joystick(joystick_number)
        self.joystick.init()

        self.axis_data = {}
        self.button_data = {}
        self.hat_data = {}

        # Initialize the data structures for buttons and axes
        for i in range(self.joystick.get_numbuttons()):
            self.button_data[i] = False

        for i in range(self.joystick.get_numaxes()):
            self.axis_data[i] = 0.0

        for i in range(self.joystick.get_numhats()):
            self.hat_data[i] = (0, 0)

        # Mapping dictionaries
        self.button_mapping = {i: self.default_button_action for i in range(self.joystick.get_numbuttons())}
        self.axis_mapping = {i: self.default_axis_action for i in range(self.joystick.get_numaxes())}
        self.hat_mapping = {i: self.default_hat_action for i in range(self.joystick.get_numhats())}

    def update(self):
        # Process pygame events
        pygame.event.pump()

        # Update button states
        for i in range(self.joystick.get_numbuttons()):
            if self.joystick.get_button(i):
                action_name = self.BUTTON_NAMES.get(i, f"Button {i}")
                print(f"{action_name} pressed")
                self.button_mapping[i]()  # Trigger the mapped action
            self.button_data[i] = self.joystick.get_button(i)

        # Update axis states
        for i in range(self.joystick.get_numaxes()):
            axis_value = self.joystick.get_axis(i)
            if i is 0 or i is 1 or i is 3 or i is 4:
                if abs(axis_value) > 0.1:  # Consider slight movement
                    action_name = self.AXIS_NAMES.get(i, f"Axis {i}")
                    print(f"{action_name} moved: {axis_value}")
                    self.axis_mapping[i](axis_value)  # Trigger the mapped action
            else:
                if axis_value > - 0.9:  # Consider slight movement
                    action_name = self.AXIS_NAMES.get(i, f"Axis {i}")
                    print(f"{action_name} moved: {axis_value}")
                    self.axis_mapping[i](axis_value)  # Trigger the mapped action
            self.axis_data[i] = axis_value

        # Update hat states (D-pad)
        for i in range(self.joystick.get_numhats()):
            hat_value = self.joystick.get_hat(i)
            if hat_value != (0, 0):
                action_name = self.HAT_NAMES.get(i, f"Hat {i}")
                print(f"{action_name} moved: {hat_value}")
                self.hat_mapping[i](hat_value)  # Trigger the mapped action
            self.hat_data[i] = hat_value

    def get_button(self, button_number):
        return self.button_data.get(button_number, False)

    def get_axis(self, axis_number):
        return self.axis_data.get(axis_number, 0.0)

    def get_hat(self, hat_number):
        return self.hat_data.get(hat_number, (0, 0))

    def remap_button(self, button_number, action):
        """Remap a button to a new action."""
        self.button_mapping[button_number] = action

    def remap_axis(self, axis_number, action):
        """Remap an axis to a new action."""
        self.axis_mapping[axis_number] = action

    def remap_hat(self, hat_number, action):
        """Remap the D-pad (hat) to a new action."""
        self.hat_mapping[hat_number] = action


    def close(self):
        self.joystick.quit()
        pygame.quit()

    def default_button_action(self):
        """Default action for unmapped buttons."""
        # print("Button pressed but no action mapped.")

    def default_axis_action(self, value):
        """Default action for unmapped axes."""
        # print(f"Axis moved but no action mapped. Value: {value}")

    def default_hat_action(self, value):
        """Default action for unmapped hat (D-pad)."""
        # print(f"Hat moved but no action mapped. Value: {value}")

def get_connected_controllers():
    controllers = []
    pygame.init()
    pygame.joystick.init()
    
    for i in range(pygame.joystick.get_count()):
        controller = XboxController(joystick_number=i)
        controllers.append(controller)
    
    return controllers
