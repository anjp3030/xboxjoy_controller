import pygame
import time

class XboxController:
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

    def update(self):
        # Process pygame events
        pygame.event.pump()

        # Update button states
        for i in range(self.joystick.get_numbuttons()):
            if self.joystick.get_button(i):
                print(f"Button {i} pressed")
            self.button_data[i] = self.joystick.get_button(i)

        # Update axis states
        for i in range(self.joystick.get_numaxes()):
            axis_value = self.joystick.get_axis(i)
            if abs(axis_value) > 0.1:  # Consider slight movement
                print(f"Axis {i} moved: {axis_value}")
            self.axis_data[i] = axis_value

        # Update hat states (D-pad)
        for i in range(self.joystick.get_numhats()):
            hat_value = self.joystick.get_hat(i)
            if hat_value != (0, 0):
                print(f"Hat {i} moved: {hat_value}")
            self.hat_data[i] = hat_value

    def get_button(self, button_number):
        return self.button_data.get(button_number, False)

    def get_axis(self, axis_number):
        return self.axis_data.get(axis_number, 0.0)

    def get_hat(self, hat_number):
        return self.hat_data.get(hat_number, (0, 0))

    def set_vibration(self, left_motor=0.0, right_motor=0.0, duration=1.0):
        """Sets the vibration for the Xbox controller.
        
        Note: Pygame does not natively support vibration. 
        You need to use an additional library like `evdev` on Linux or other platform-specific libraries.
        
        This method is a placeholder to illustrate where vibration logic would be implemented.
        """
        print(f"Vibration - Left motor: {left_motor}, Right motor: {right_motor} for {duration} seconds")
        time.sleep(duration)
        # Reset the vibration
        print("Vibration off")

    def close(self):
        self.joystick.quit()
        pygame.quit()

# Multi-controller support
def get_connected_controllers():
    controllers = []
    pygame.init()
    pygame.joystick.init()
    
    for i in range(pygame.joystick.get_count()):
        controller = XboxController(joystick_number=i)
        controllers.append(controller)
    
    return controllers

def main():
    try:
        controllers = get_connected_controllers()
        
        if not controllers:
            print("No controllers found.")
            return
        
        # For simplicity, just using the first controller
        controller = controllers[0]

        while True:
            controller.update()

            time.sleep(0.1)
    
    except Exception as e:
        print(str(e))
    
    finally:
        for controller in controllers:
            controller.close()

if __name__ == "__main__":
    main()
