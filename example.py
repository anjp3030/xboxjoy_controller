from xbox_controller import get_connected_controllers
import time
def main():
    try:
        controllers = get_connected_controllers()
        
        if not controllers:
            print("No controllers found.")
            return
        
        # For simplicity, just using the first controller
        controller = controllers[0]

        # Example of remapping button and axis actions
        # controller.remap_button(0, lambda: print("Jump action triggered!"))
        # controller.remap_button(1, lambda: print("Shoot action triggered!"))
        # controller.remap_axis(0, lambda value: print(f"Moving left/right with intensity: {value}"))
        # controller.remap_axis(1, lambda value: print(f"Moving up/down with intensity: {value}"))
        # controller.remap_hat(0, lambda value: print(f"D-pad moved to: {value}"))

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
