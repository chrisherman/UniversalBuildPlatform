"""
	Publihsed under MIT License, 2026
	Original Author: chrisherman@simplestuffmatters.com
"""


import adsk.core, adsk.fusion, traceback

handlers = []

def build_node_geometry(sketch, n_nodes, height_cm):
    """
    Constructs n contiguous cells along the X-axis using DXF geometry coordinates.
    Converts mm to cm (Fusion internal unit).
    """
    lines = sketch.sketchCurves.sketchLines
    
    # Internal units (cm) derived from DXF (14mm x 5mm cell)
    cell_w = 1.400       # 14.00 mm
    top_y = 0.500        # 5.00 mm
    
    # Offsets along cell width
    top_left_x = 0.2025    # 2.025 mm
    bot_left_x = 0.5025    # 5.025 mm
    bot_right_x = 0.8975   # 8.975 mm
    top_right_x = 1.1975   # 11.975 mm

    total_length = n_nodes * cell_w
    bottom_y = -height_cm

    # 1. Outer Box (Left, Bottom, Right) extending by 'height'
    lines.addByTwoPoints(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(0, bottom_y, 0)
    )
    lines.addByTwoPoints(
        adsk.core.Point3D.create(0, bottom_y, 0),
        adsk.core.Point3D.create(total_length, bottom_y, 0)
    )
    lines.addByTwoPoints(
        adsk.core.Point3D.create(total_length, bottom_y, 0),
        adsk.core.Point3D.create(total_length, 0, 0)
    )

    # 2. Generate repeating top geometry across all n nodes
    for i in range(n_nodes):
        x0 = i * cell_w

        # Left bottom flat wing
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x0, 0, 0),
            adsk.core.Point3D.create(x0 + bot_left_x, 0, 0)
        )
        # Angled left slope
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x0 + bot_left_x, 0, 0),
            adsk.core.Point3D.create(x0 + top_left_x, top_y, 0)
        )
        # Top gap flat bridge
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x0 + top_left_x, top_y, 0),
            adsk.core.Point3D.create(x0 + top_right_x, top_y, 0)
        )
        # Angled right slope
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x0 + top_right_x, top_y, 0),
            adsk.core.Point3D.create(x0 + bot_right_x, 0, 0)
        )
        # Right bottom flat wing
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x0 + bot_right_x, 0, 0),
            adsk.core.Point3D.create(x0 + cell_w, 0, 0)
        )

    return sketch.profiles.item(0)


class CustomCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            command = args.firingEvent.sender
            inputs = command.commandInputs
            
            nodes_input = adsk.core.IntegerSliderCommandInput.cast(inputs.itemById('nodes_input'))
            width_input = adsk.core.ValueCommandInput.cast(inputs.itemById('width_input'))
            height_input = adsk.core.ValueCommandInput.cast(inputs.itemById('height_input'))

            n_nodes = nodes_input.valueOne
            width_val = width_input.value   # cm
            height_val = height_input.value # cm

            app = adsk.core.Application.get()
            design = adsk.fusion.Design.cast(app.activeProduct)
            root_comp = design.rootComponent

            sketch = root_comp.sketches.add(root_comp.xYConstructionPlane)
            profile = build_node_geometry(sketch, n_nodes, height_val)

            extrudes = root_comp.features.extrudeFeatures
            distance = adsk.core.ValueInput.createByReal(width_val)
            extrudes.addSimple(
                profile, 
                distance, 
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )

        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class CustomCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # Terminate script execution when command dialog closes (OK or Cancel)
            adsk.terminate()
        except:
            pass


class CustomCommandValidateInputsHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            event_args = adsk.core.ValidateInputsEventArgs.cast(args)
            inputs = event_args.inputs
            
            width_input = adsk.core.ValueCommandInput.cast(inputs.itemById('width_input'))
            height_input = adsk.core.ValueCommandInput.cast(inputs.itemById('height_input'))

            if width_input.value <= 0 or height_input.value <= 0:
                event_args.areInputsValid = False
            else:
                event_args.areInputsValid = True
        except:
            pass


class CustomCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            cmd = adsk.core.Command.cast(args.command)
            inputs = cmd.commandInputs

            # 1. Number of Nodes (1-100, default 3)
            slider = inputs.addIntegerSliderCommandInput('nodes_input', 'Number of Nodes (n)', 1, 100)
            slider.valueOne = 3

            # 2. Width Input (>0, default 10mm)
            inputs.addValueInput('width_input', 'Width', 'mm', adsk.core.ValueInput.createByString('10 mm'))

            # 3. Height Input (>0, default 1mm)
            inputs.addValueInput('height_input', 'Height', 'mm', adsk.core.ValueInput.createByString('1 mm'))

            # Attach event handlers
            on_execute = CustomCommandExecuteHandler()
            cmd.execute.add(on_execute)
            handlers.append(on_execute)

            on_validate = CustomCommandValidateInputsHandler()
            cmd.validateInputs.add(on_validate)
            handlers.append(on_validate)

            on_destroy = CustomCommandDestroyHandler()
            cmd.destroy.add(on_destroy)
            handlers.append(on_destroy)

        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def run(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        cmd_def = ui.commandDefinitions.itemById('UniversalMountingSystemCmd')
        if not cmd_def:
            cmd_def = ui.commandDefinitions.addButtonDefinition(
                'UniversalMountingSystemCmd', 
                'Universal Mounting System', 
                'Generates extruded multi-node array with height extension'
            )

        on_created = CustomCommandCreatedHandler()
        cmd_def.commandCreated.add(on_created)
        handlers.append(on_created)

        cmd_def.execute()

        # Keep alive while dialog is active
        adsk.autoTerminate(False)

    except:
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))