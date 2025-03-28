from streamlit_option_menu import option_menu
import streamlit as st
import json
import os
from datetime import datetime

# Define file paths
TODO_TASK = "todo.json"
RECYCLE_BIN_FILE = "recycle_bin.json"
color_priority = {"red": "#DD111B", "yellow": "orange", "green": "#00C923"}


def load_todo():
    """Load tasks from the JSON file."""
    if os.path.exists(TODO_TASK):
        with open(TODO_TASK, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_todo(todo):
    """Save tasks to the JSON file."""
    with open(TODO_TASK, "w") as file:
        json.dump(todo, file, indent=4)


def load_recycle():
    """Load tasks from the recycle bin."""
    if os.path.exists(RECYCLE_BIN_FILE):
        with open(RECYCLE_BIN_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_recycle(todo):
    """Save tasks to the recycle bin."""
    with open(RECYCLE_BIN_FILE, "w") as file:
        json.dump(todo, file, indent=4)


# Load tasks
todo = load_todo()


# Main Menu
selected = option_menu(
    menu_title=None,
    options=["Add", "Display", "Edit", "Delete", "Restore"],
    icons=["plus-circle", "list-ul", "pencil",
           "trash", "arrow-counterclockwise"],
    menu_icon="menu-button-wide",
    default_index=0,
    orientation="horizontal"
)
# Main Title
st.markdown(
    "<p style='text-align: center; line-height: 10px; color: gray; letter-spacing: 8px; font-weight: 100'>Welcome to your</p>",
    unsafe_allow_html=True)
st.markdown(
    "<h1 style='text-align: center; line-height: 10px;'>🎯 To-Do List Manager</h1>",
    unsafe_allow_html=True)

if selected == "Add":
    # SubHeading
    st.markdown(
        "<h5 style='text-align: center; line-height: 15px; margin-top: 20px;color: #AC92EB; font-weight: 400'>Quickly add a new task to your list</h5>",
        unsafe_allow_html=True)

    # Inputs for Adding a New Task in Columns
    col1_add, col2_add = st.columns([1, 1])

    # Input for Task Title
    with col1_add:
        add_title = st.text_input(":gray[Enter the task title:]",
                                  placeholder="e.g. Complete AI Project")

    # Input for Task Priority
    with col2_add:
        add_priority = st.selectbox(":gray[Select task priority:]", [
                                    "Low", "Medium", "High"])

    col3_add, col4_add = st.columns([1, 1])

    # Input for Due Date
    with col3_add:
        add_due_date = st.date_input(
            ":gray[Select due date:]").strftime("%d-%b-%Y")

    # Input for Completion Status
    with col4_add:
        add_completed = st.selectbox(
            ":gray[Is the task completed?]", ["No", "Yes"])

    # Input for Task Details
    add_details = st.text_area(":gray[Enter task details:]",
                               placeholder="e.g. Research and implement AI model")

    # Save New Task Button
    if st.button(":green[✚ Add Task]"):
        # Check if Title is Duplicate
        is_duplicate = any(task["title"].lower() ==
                           add_title.lower() for task in todo)

        # Validate Inputs (Ensure all fields are filled)
        if add_title and add_priority and add_due_date and add_details and add_completed:
            if is_duplicate:
                st.error("❌ Task title already exists! Try a different title.")
            else:
                added_date = datetime.today().strftime("%Y-%m-%d %I:%M:%S %p")
                # Create a new Task entry
                new_task = {
                    "title": add_title,
                    "details": add_details,
                    "due date": str(add_due_date),  # Convert date to string
                    "priority": add_priority,
                    "completed": add_completed,
                    "added date": added_date
                }
                # Append and Save
                todo.append(new_task)
                save_todo(todo)
                # Success Message
                st.success(f"✅ Task ❝{add_title}❞ added successfully!")
        else:
            st.error("❌ Please fill in all fields before adding the task.")


if selected == "Display":
    # SubHeading
    st.markdown(f"<h5 style='text-align: center; line-height: 15px; margin-top: 20px;color: #AC92EB; font-weight: 400'>View all your tasks at a glance</h5>", unsafe_allow_html=True)
    # If todo is Empty
    if not todo:
        st.markdown(
            f"<div style='display: flex; justify-content: center; align-items: center; background: linear-gradient(135deg, red, green); padding: 20px 10px; margin: 30px 0px; border-radius: 5px; color: white; font-weight: 100;'>⊘ Your to-do list is currently empty. Add a task to get started.</div>",
            unsafe_allow_html=True)
    else:
        priority = ""
        is_completed = ""
        remaining_days = ""
        remaining_result = ""
        opacity = "opacity: 1; background-color: #0e1117;"
        for index, task in enumerate(todo, start=1):
            # Check Priority
            if task["priority"] == "Low":
                priority = color_priority["green"]
            elif task["priority"] == "Medium":
                priority = color_priority["yellow"]
            elif task["priority"] == "High":
                priority = color_priority["red"]
            # Check Completed of Not
            if task["completed"] == "Yes":
                is_completed = "✅"
            elif task["completed"] == "No":
                is_completed = "❌"
            # Check Expired or not
            due_date = datetime.strptime(task["due date"], "%d-%b-%Y").date()
            today_date = datetime.today().date()
            remaining_days = (due_date - today_date).days
            if remaining_days < 0:
                remaining_result = "Expired!"
                opacity = "opacity: 0.3;background-color: black;"
            elif remaining_days == 0:
                remaining_result = "Today!"
                opacity = "opacity: 1; border: 1px solid #262730"
            elif remaining_days == 1:
                remaining_result = "Tomorrow!"
                opacity = "opacity: 1; border: 1px solid #262730"
            else:
                remaining_result = f"{remaining_days} days!"
                opacity = "opacity: 1; border: 1px solid #262730"

            st.markdown(
                f"""<div
      style="
        display: grid;
        grid-template-columns: 20px 20px 150px 2fr 100px 55px;
        align-items: center;
        justify-content: space-between;
        padding: 5px 10px;
        border-radius: 10px;
        margin: 5px 0px;
        {opacity}
      "
    >
      <p style="color: gray;">{index}.</p>
      <p>{is_completed}</p>
      <div style="padding: 0px 10px">
        <p style="font-weight: 800; font-size: large; white-space: nowrap;overflow: hidden;text-overflow: ellipsis;">{task["title"]}</p>
        <p style="color: gray; opacity: 0.7; font-size: 10px; line-height: 10px">
          {task["added date"]}
        </p>
      </div>
      <p style="font-size: 12px; padding: 0px 10px; opacity:0.8;">
        {task["details"]}
      </p>
      <div style="text-align: center;">
        <p style="font-size: 12px; line-height: 10px">{task["due date"]}</p>
        <p style="color: gray;font-size: 10px; line-height: 10px ">{remaining_result}</p>
      </div>
      <p
        style="
          background-color: {priority};
          color: white;
          padding: 3px 4px;
          border-radius: 5px;
          text-align: center;
          font-size: 12px
        "
      >
        {task["priority"]}
      </p>
    </div>""", unsafe_allow_html=True)


if selected == "Edit":
    # SubHeading
    st.markdown(f"<h5 style='text-align: center; line-height: 15px; margin-top: 20px;color: #AC92EB; font-weight: 400'>Modify your tasks with ease</h5>", unsafe_allow_html=True)
    # If todo is Empty
    if not todo:
        st.markdown(
            f"<div style='display: flex; justify-content: center; align-items: center; background: linear-gradient(135deg, red, green); padding: 20px 10px; margin: 30px 0px; border-radius: 5px; color: white; font-weight: 100;'>⊘ Your to-do list is currently empty. Add a task to get started.</div>",
            unsafe_allow_html=True)
    else:
        task_titles = [task["title"] for task in todo]
        task_to_edit = st.selectbox(
            "✏️ :gray[Select a task to edit:]", task_titles)
        st.markdown("""<p style="color: yellow; text-align:center;">⚙️ Make changes below</p>""",
                    unsafe_allow_html=True)

        # Inputs for Adding a New Task in Columns
        col1_add, col2_add = st.columns([1, 1])
        task = next(task for task in todo if task["title"] == task_to_edit)

        # Input for Task Title
        with col1_add:
            new_title = st.text_input(":gray[📌 Task Title:]",
                                      task_to_edit)

        # Input for Task Priority
        with col2_add:
            new_priority = st.selectbox(":gray[⚡ Priority:]", [
                                        "Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task["priority"]))

        col3_add, col4_add = st.columns([1, 1])

        # Input for Due Date
        with col3_add:
            new_due_date = st.date_input(
                ":gray[📆 Due Date:]", datetime.strptime(task["due date"], "%d-%b-%Y")).strftime("%d-%b-%Y")

        # Input for Completion Status
        with col4_add:
            new_completed = st.selectbox(
                ":gray[✔️ Completion Status:]", ["No", "Yes"], index=["No", "Yes"].index(task["completed"]))

        # Input for Task Details
        new_details = st.text_area(":gray[📜 Task Details:]",
                                   task["details"])

        # Save New Task Button
        if st.button(":green[⎙ Save Changes]"):
            task.update({
                "title": new_title,
                "priority": new_priority,
                "due date": new_due_date,
                "completed": new_completed,
                "details": new_details
            })
            save_todo(todo)
            st.success(f"✅ Task '{new_title}' updated successfully!")
if selected == "Delete":
    # SubHeading
    st.markdown(f"<h5 style='text-align: center; line-height: 15px; margin-top: 20px;color: #AC92EB; font-weight: 400'>Remove tasks and send them to the recycle bin</h5>", unsafe_allow_html=True)
    # If todo is Empty
    if not todo:
        st.markdown(
            f"<div style='display: flex; justify-content: center; align-items: center; background: linear-gradient(135deg, red, green); padding: 20px 10px; margin: 30px 0px; border-radius: 5px; color: white; font-weight: 100;'>⊘ Your to-do list is currently empty. Add a task to get started.</div>",
            unsafe_allow_html=True)
    else:
        task_titles = [task["title"] for task in todo]
        task_to_delete = st.selectbox(
            "🗑️ Select a task to delete:", task_titles)

        if st.button("🚮 Delete Task"):
            deleted_task = next(
                task for task in todo if task["title"] == task_to_delete)
            todo.remove(deleted_task)
            recycle_bin = load_recycle()
            recycle_bin.append(deleted_task)
            save_todo(todo)
            save_recycle(recycle_bin)
            st.success(f"❌ Task '{task_to_delete}' moved to recycle bin.")
if selected == "Restore":
    # SubHeading
    st.markdown(f"<h5 style='text-align: center; line-height: 15px; margin-top: 20px;color: #AC92EB; font-weight: 400'>Recover deleted tasks from the recycle bin</h5>", unsafe_allow_html=True)
    recycle_bin = load_recycle()
    # If todo is Empty
    if not recycle_bin:
        st.markdown(
            f"<div style='display: flex; justify-content: center; align-items: center; background: linear-gradient(135deg, red, green); padding: 20px 10px; margin: 30px 0px; border-radius: 5px; color: white; font-weight: 100;'>⊘ Your to-do list is currently empty. Add a task to get started.</div>",
            unsafe_allow_html=True)
    else:
        task_titles = [task["title"] for task in recycle_bin]
        task_to_restore = st.selectbox(
            "♻️ Select a task to restore:", task_titles)

        if st.button("🔄 Restore Task"):
            restored_task = next(
                task for task in recycle_bin if task["title"] == task_to_restore)
            recycle_bin.remove(restored_task)
            todo.append(restored_task)
            save_todo(todo)
            save_recycle(recycle_bin)
            st.success(f"✅ Task '{task_to_restore}' restored successfully!")


# CSS Properties if Required
st.markdown("""
    <style>
        input::placeholder {font-size: 14px !important; font-weight: 100 !important;}
    </style>
""", unsafe_allow_html=True)


# Footer
st.markdown("""<p style="color: #2f3038; text-align:center;">Made with ❤ by Zubair Ahmed</p>""",
            unsafe_allow_html=True)