import os

import libqtile.resources
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"

#USER DEFINED START
import math
import psutil
import subprocess
from libqtile import hook, images
from libqtile.widget import base

@hook.subscribe.startup_once
def run_at_start():
    home = os.path.expanduser("~")
    start_apps = os.path.join(home, ".config", "qtile", "scripts", "autostart.sh")
    subprocess.Popen([start_apps])

terminal = "alacritty"
browser = "google-chrome-stable"
app_list = "rofi -show drun"

#USER DEFINED END


#terminal = guess_terminal()

keys = [
    #USER DEFINED START
    Key([mod], "a", lazy.spawn(browser), desc="Launch Chrome"),
    Key([mod], "d", lazy.spawn(app_list), desc="Launch Rofi"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 2"), desc="Increase volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 2"), desc="Decrease volume"),
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t"), desc="Toggle mute"),
    Key([mod], "Print", lazy.spawn("flameshot gui")),
    Key([mod, "shift"], "Print", lazy.spawn("flameshot full --path /home/macxz/Pictures/screenshots")),
    Key([mod, "shift"], "w", lazy.spawn("betterlockscreen -l dimblur"), desc="Lock screen"),
    #USER DEFINED END
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

for i in range(1, 7):
    keys.append(
        Key([mod], str(i), lazy.group[str(i)].toscreen())
    )

for i in range(1, 7):
    keys.append(
        Key([mod, "shift"], str(i), lazy.window.togroup(str(i)))
    )

layout_theme = {
    "margin": 7,
    "border_width": 1,
    "border_focus": "4fb2a2",
    "border_normal": "272d89",
    }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max()
]

# DEFINE HDD STORAGE
def hdd_usage():
    usage = psutil.disk_usage("/")
    return f"  \n {usage.percent}%"
def hdd_home_usage():
    usage = psutil.disk_usage("/home")
    return f"  \n {usage.percent}%"

# DEFINE WIDGET THEMES
widget_theme_white = {
    "foreground": "ffffff",
    "font": "Mononoki Nerd Font",
    "fontsize": 20,
}

widget_theme_bluish = {
    "foreground": "4fb2a2",
    "font": "Mononoki Nerd Font",
    "fontsize": 16,
}

widget_right_clickable = {
    "foreground":"ffffff",
    "font":"Mononoki Nerd Font",
    "fontsize":14,
}
widget_right_unclickable = {
    "foreground":"4fb2a2",
    "font":"Mononoki Nerd Font",
    "fontsize":14,
}

# WIFI STATUS MOD
class DistinctWlan(widget.Wlan):
    def poll(self):
        try:
            # Check radio state
            radio = subprocess.check_output(
                ["nmcli", "radio", "wifi"], text=True
            ).strip()
            if radio == "disabled":
                return "󰖪  "  # radio off icon

            # Otherwise, fall back to normal Wlan logic
            base = super().poll() or "󱚿 "
            if base.strip().lower() == "disconnected":
                return "󱚿  "  # disconnected icon
            return base
        except Exception:
            return "?"

wifi_functions = {
    "Button1": lazy.spawn("sh -c '$HOME/.config/polybar/scripts/wifi_connect.sh'"),
    "Button2": lazy.spawn("sh -c '$HOME/.config/polybar/scripts/wifi_on.sh'"),
    "Button3": lazy.spawn("sh -c '$HOME/.config/polybar/scripts/wifi_off.sh'"),
}

# WORKSPACE CONDITIONS
groups = []

group_icon_active = ["󰇊","󰇋", "󰇌", "󰇍", "󰇎", "󰇏"]
group_icon_inactive = ["󱅊", "󱅋", "󱅌", "󱅍", "󱅎", "󱅏"]
group_names = ["1", "2", "3", "4", "5", "6"]
group_labels = ["󰇊","󰇋", "󰇌", "󰇍", "󰇎", "󰇏"]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i]
        )
    )

for group in groups:
    keys.extend([
        Key([mod], group.name, lazy.group[group.name].toscreen(),
            desc=f"Switch to group {group.name}"),
        Key([mod, "shift"], group.name, lazy.window.togroup(group.name),
            desc=f"Move focused window to group {group.name}"),
    ])

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=10),
                widget.TextBox(
                    text="󰏚 ",
                    **widget_theme_white,
                ),
                widget.GroupBox(
                    **widget_theme_white,
                    highlight_method='line',
                    highlight_color=['00000000', '00000000'],
                    inactive='4fb2a2',
                    hide_unused=True,
                    this_current_screen_border='4fb2a2',
                    urgent_border='4fb2a280',
                    urgent_text='252251'
                ),
                widget.Spacer(),
                widget.CPU(
                    **widget_right_unclickable,
                    format=' \n{load_percent}%'
                ),
                widget.Memory(
                    **widget_right_unclickable,
                    format="󰧑 \n{MemPercent}%",
                ),
                widget.TextBox(
                    **widget_right_unclickable,
                    text=hdd_usage(),
                ),
                widget.TextBox(
                    **widget_right_unclickable,
                    text=hdd_home_usage(),
                ),
                widget.Spacer(length=10),
                widget.CheckUpdates(
                    **widget_right_clickable,
                    colour_have_updates='fe4dcc',
                    colour_no_updates='ffffff',
                    display_format='󱧘 \n{updates}',
                    no_update_string='󱧖 \n0 ',
                    update_interval=60,
                    mouse_callbacks={
                        "Button1": lazy.spawn("alacritty -e sudo pacman -Syu")
                    }
                ),
                widget.Volume(
                    **widget_right_clickable,
                    unmute_format=' \n{volume}%',
                    mute_format=' ',
                    mouse_callbacks={
                        "Button2": lazy.spawn("pavucontrol")
                    },
                ),
                DistinctWlan(
                    **widget_right_clickable,
                    ethernet_interface='enp0s31f6',
                    ethernet_message_format='󰈀 ',
                    format='󱚽 \n{percent:2.0%}',
                    use_ethernet=True,
                    update_interval=1,
                    mouse_callbacks=wifi_functions,
                ),
                widget.Spacer(length=10),            
                widget.Clock(
                    **widget_right_unclickable,
                    format="%m/%d/%y %a\n%I:%M:%S %p",
                    ),
                widget.TextBox(
                    text=" ⏻ ",
                    **widget_theme_white,
                    mouse_callbacks={
                        "Button1": lazy.spawn("sh -c '$HOME/.config/polybar/scripts/power_menu.sh'")
                    }),
                widget.Spacer(length=10),
            ],
            36,
            background="#25225159",
            margin=[7, 7, 0, 7],
            border_color="272d8959",
            border_width=1,
        ),
    ),
]


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
#dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
