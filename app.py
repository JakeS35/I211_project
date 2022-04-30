from crypt import methods
from flask import Flask, render_template, redirect, url_for, request

import csv  # Used for reading and writing event data via csv.

app = Flask(__name__)

CLASSES_PATH = app.root_path + '/classes.csv'
CLASSES_KEYS = ['name', 'date', 'duration', 'type', 'level', 'trainer', 'desc']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classes/')
def list_events():
    events = get_events()
    return render_template('classes.html', events=events)

@app.route('/classes/<class_id>/')
def view_event(class_id=None):
    if class_id:
        class_id = int(class_id)
        events = get_events()
        return render_template('class.html', class_id=class_id, event=events[class_id])
    else:
        return redirect(url_for('list_events'))

@app.route('/classes/create', methods=['GET', 'POST'])
def create_event(event=None):
    if request.method == 'POST':
        events = get_events()
        event = {}
        event['name'] = request.form['name']
        event['date'] = request.form['date']
        event['duration'] = request.form['duration']
        event['type'] = request.form['type']
        event['level'] = request.form['level']
        event['trainer'] = request.form['trainer']
        event['desc'] = request.form['desc']
        events.append(event)
        
        # Make sure events are sorted by date.
        events = sorted(events, key=lambda e: e['date'])

        # Write data back out to csv.
        set_events(events)

        # Return to the list of events.
        return redirect(url_for('list_events'))
    else:
        return render_template('class_form.html')

@app.route('/classes/<class_id>/edit', methods=['GET', 'POST'])
def edit_event(class_id=None):
    if request.method== 'POST':
       events = get_events() 
       class_id=int(class_id)
       events[class_id]['name'] = request.form['name']
       events[class_id]['date'] = request.form['date']
       events[class_id]['duration'] = request.form['duration']
       events[class_id]['type'] = request.form['type']
       events[class_id]['level'] = request.form['level']
       events[class_id]['trainer'] = request.form['trainer']
       events[class_id]['desc'] = request.form['desc']
       set_events(events)
       return redirect(url_for('view_event', class_id=class_id)) 
    else:
        if class_id:
            class_id = int(class_id)
            events = get_events()
            event=events[class_id]
        return render_template('class_form.html', class_id=class_id, event=event)

@app.route('/classes/<class_id>/delete', methods=['GET', "POST"])
def delete_event(class_id=None):
    if class_id:
        class_id = int(class_id)
        delete=request.args.get('delete', None)
        events = get_events()
        if delete == "1" and class_id < len(events):
            del events[class_id]
            set_events(events)
            return redirect(url_for('list_events'))  
        else:
            event=events[class_id]
            return render_template('delete_form.html', class_id=class_id, event=event)          
    else:
        return redirect(url_for('list_events'))

def get_events():
    results = []
    try:
        with open(CLASSES_PATH) as csv_file:
            reader = csv.DictReader(csv_file)
            results = list(reader)
    except Exception as err:
        print(err)
    return results

def set_events(events):
    try:
        with open(CLASSES_PATH, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CLASSES_KEYS)
            writer.writeheader()
            for event in events:
                writer.writerow(event)
    except Exception as err:
        print(err)

if __name__ == '__main__':
    app.run(debug = True)