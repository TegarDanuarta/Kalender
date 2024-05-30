import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QInputDialog, QCalendarWidget
from PyQt5.QtCore import QDate, QTimer


class SmartCalendar(QMainWindow):
    def _init_(self):
        super()._init_()

        self.setWindowTitle("Smart Calendar")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.calendar = QCalendarWidget(self)
        self.calendar.clicked[QDate].connect(self.show_event)
        self.layout.addWidget(self.calendar)

        self.event_label = QLabel(self)
        self.layout.addWidget(self.event_label)

        self.add_event_button = QPushButton("Add Event", self)
        self.add_event_button.clicked.connect(self.add_event)
        self.layout.addWidget(self.add_event_button)

        self.add_task_button = QPushButton("Add Task", self)
        self.add_task_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_task_button)

        self.notification_label = QLabel(self)
        self.layout.addWidget(self.notification_label)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.events = {}
        self.tasks = {}

        self.set_theme_style()

        # Timer for event and task reminders
        self.event_timer = QTimer(self)
        self.event_timer.timeout.connect(self.remind_event)
        self.task_timer = QTimer(self)
        self.task_timer.timeout.connect(self.remind_task)

        # Timer for weather update
        self.weather_timer = QTimer(self)
        self.weather_timer.timeout.connect(self.update_weather)

        # Set timers interval (milliseconds)
        self.event_timer_interval = 60 * 1000  # 1 minute
        self.task_timer_interval = 60 * 1000  # 1 minute
        self.weather_timer_interval = 30 * 60 * 1000  # 30 minutes

        # Start timers
        self.event_timer.start(self.event_timer_interval)
        self.task_timer.start(self.task_timer_interval)
        self.weather_timer.start(self.weather_timer_interval)

    def show_event(self, date):
        event_date = date.toString("yyyy-MM-dd")
        if event_date in self.events:
            self.event_label.setText("Event: " + self.events[event_date])
        elif event_date in self.tasks:
            self.event_label.setText("Task: " + self.tasks[event_date])
        else:
            self.event_label.setText("No events or tasks for this date.")

    def add_event(self):
        event_date, ok = QInputDialog.getText(self, "Add Event", "Enter date (YYYY-MM-DD):")
        if ok:
            event_name, ok = QInputDialog.getText(self, "Add Event", "Enter event name:")
            if ok:
                self.events[event_date] = event_name
                self.show_event(QDate.fromString(event_date, "yyyy-MM-dd"))
                # Set reminder for event
                self.set_event_reminder(event_date)

    def add_task(self):
        task_date, ok = QInputDialog.getText(self, "Add Task", "Enter date (YYYY-MM-DD):")
        if ok:
            task_name, ok = QInputDialog.getText(self, "Add Task", "Enter task name:")
            if ok:
                self.tasks[task_date] = task_name
                self.show_event(QDate.fromString(task_date, "yyyy-MM-dd"))
                # Set reminder for task
                self.set_task_reminder(task_date)

    def set_theme_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0; /* Light Gray */
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: black;
                selection-background-color: #4d94ff; /* Light Blue */
            }
            QPushButton {
                background-color: #4d94ff; /* Light Blue */
                color: white;
                border: 1px solid #4d94ff;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0059b3; /* Darker Blue */
            }
            QLabel {
                color: #333;
            }
        """)

    def set_event_reminder(self, event_date):
        # Calculate time until event in milliseconds
        event_datetime = QDate.fromString(event_date, "yyyy-MM-dd")
        current_date = QDate.currentDate()
        time_until_event = current_date.daysTo(event_datetime) * 24 * 60 * 60 * 1000

        # Start timer for event reminder
        self.event_timer.start(time_until_event)
        self.event_timer.setObjectName(event_date)

    def set_task_reminder(self, task_date):
        # Calculate time until task in milliseconds
        task_datetime = QDate.fromString(task_date, "yyyy-MM-dd")
        current_date = QDate.currentDate()
        time_until_task = current_date.daysTo(task_datetime) * 24 * 60 * 60 * 1000

        # Start timer for task reminder
        self.task_timer.start(time_until_task)
        self.task_timer.setObjectName(task_date)

    def remind_event(self):
        event_date = self.event_timer.objectName()
        event_name = self.events[event_date]
        self.notification_label.setText(f"Reminder: Event '{event_name}'")

    def remind_task(self):
        task_date = self.task_timer.objectName()
        task_name = self.tasks[task_date]
        self.notification_label.setText(f"Reminder: Task '{task_name}'")

    def update_weather(self):
        # Placeholder for weather update
        weather_info = "Weather: Sunny, 25°C"
        self.notification_label.setText(weather_info)


if _name_ == "_main_":
    app = QApplication(sys.argv)
    calendar = SmartCalendar()
    calendar.show()
    sys.exit(app.exec_())