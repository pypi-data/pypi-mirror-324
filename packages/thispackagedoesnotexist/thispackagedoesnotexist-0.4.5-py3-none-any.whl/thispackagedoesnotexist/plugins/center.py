def CenterWindowToDisplay(root, width, height):
    try:
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        scale_factor = root._get_window_scaling()
        x = int(((screen_width / 2) - (width / 2)) * scale_factor)
        y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)
        return f"{width}x{height}+{x}+{y}"
    except:
        pass