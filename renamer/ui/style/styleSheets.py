# ui/stylesheets.py

MAYA_STYLE = """
QWidget
{
    background-color: #3a3a3a;
    color: #d6d6d6;
    font-size: 9pt;
}

/* Inputs */

QLineEdit,
QSpinBox
{
    background-color: #2b2b2b;
    border: 1px solid #4a4a4a;
    padding: 3px;
    min-height: 18px;
}

QLineEdit:focus,
QSpinBox:focus
{
    border: 1px solid #0f5560;
}

/* Buttons */

QPushButton
{
    background-color: #083844;
    border: 1px solid #144550;
    padding: 4px;
    min-height: 20px;
}

QPushButton:hover
{
    background-color: #0c4b58;
}

QPushButton:pressed
{
    background-color: #072e37;
}

/* Suffix buttons */

QPushButton[quickSuffix="true"]
{
    background-color: #23444a;
}

QPushButton[quickSuffix="true"]:hover
{
    background-color: #2d5960;
}

/* Color buttons */

QPushButton[colorButton="true"]
{
    border: 1px solid #222;
    min-height: 22px;
}

/* Radio Buttons */

QRadioButton
{
    spacing: 5px;
}

QRadioButton::indicator
{
    width: 12px;
    height: 12px;
}

/* Slider */

QSlider::groove:horizontal
{
    background: #2a2a2a;
    height: 6px;
}

QSlider::handle:horizontal
{
    background: #c0c0c0;
    width: 10px;
    margin: -5px 0;
}

/* Group Boxes */

QGroupBox
{
    border: 1px solid #555;
    margin-top: 6px;
    padding-top: 8px;
}

QGroupBox::title
{
    subcontrol-origin: margin;
    left: 10px;
}

/* Selection / utility buttons */

QPushButton[selectionButton="true"]
{
    background-color: #083844;
    border: 1px solid #144550;
    padding: 2px;
    min-height: 18px;
}

QPushButton[selectionButton="true"]:hover
{
    background-color: #0c4b58;
}

QPushButton[selectionButton="true"]:pressed
{
    background-color: #072e37;
}

QPushButton[selectionWideButton="true"]
{
    background-color: #083844;
    border: 1px solid #144550;
    padding: 2px;
    min-height: 18px;
}

QPushButton[selectionWideButton="true"]:hover
{
    background-color: #0c4b58;
}

QPushButton[selectionWideButton="true"]:pressed
{
    background-color: #072e37;
}

/* Selection preset list */

QListWidget[selectionPresetList="true"]
{
    background-color: #2b2b2b;
    border: 1px solid #4a4a4a;
    padding: 1px;
}

QListWidget[selectionPresetList="true"]::item
{
    min-height: 16px;
    padding: 1px 3px;
}

QListWidget[selectionPresetList="true"]::item:selected
{
    background-color: #0c4b58;
    color: #ffffff;
}

/* Small section title labels */

QLabel[sectionTitle="true"]
{
    color: #dcdcdc;
    font-weight: bold;
}
"""