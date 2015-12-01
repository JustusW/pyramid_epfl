.. _tutorial_1:

Tutorial Part 1: Basic Notes App
================================

In this tutorial, we create a simple EPFL app that provides a simple functionality to create, edit and delete notes.
For this reason, the app simply provides one view.

First, we start by creating and setting up the demo app based on an empty EPFL starter pyramid scaffold.
We create the demo app, run setup.py to set it up, and launch it using the pserve command.


.. code-block:: bash

    pcreate -s pyramid_epfl_starter demo_app
    cd demo_app/
    python setup.py develop
    pserve development.ini --reload

The app is now running on localhost:8080. If you open the URL, you will see a simple empty page displaying a "Welcome to EPFL!" message.
We will now extend this app to add the notes functionality.

You can view the final results of the complete tutorial) in a different scaffold:

.. code-block:: bash

    pcreate -s pyramid_epfl_tutorial tutorial_app
    cd tutorial_app/
    python setup.py develop
    pserve development.ini --reload
    
If you want to view both the final tutorial app and your working version (demo_app), change the port in the development.ini file 
of the tutorial app to run both server instances in parallel on your machine. 

Let's go back to our empty notes app. In demo_app/epf_pyramid_barebone/views/home.py, we will do most of the work.

In this file, we start by adding a navbar to the root component. The root component is the component that 
resides directly on the page and is basically responsible for the overall layout of the page.

In home.py, we see that the root component is instantiated as follows:

.. code-block:: python

	@view_config(route_name='home')
	class HomePage(epfl.Page):
	    root_node = HomeRoot(constrained=True, node_list=[epfl.components.Box(title="Welcome to EPFL!")])
	    
We change this by setting different attributes to the root_node HomeRoot object: 

.. code-block:: python

	from solute.epfl.components import NavLayout

	@view_config(route_name='home')
	class HomePage(epfl.Page):
	    root_node = HomeRoot(constrained=True, node_list=[NavLayout(slot='north', title='Demo Notes App')])

This replaces the box with the welcome message by a simple navbar that contains a "home" button named "Demo Notes App".
Note that by setting slot="north" in the NavLayout component, we told EPFL that this component is going to be placed in the 
top area of the parent component (this is possible since HomeRoot inherits from CardinalLayout which provides this functionality).

A lot of EPFL's components are so-called container components. They support nested components that are stored in the component's node_list attribute.

Next, we will add another component to the root component: the component that will display the form where we can create a new note or
edit an existing one.
We could do this by just extending note_list with further components when instantiating the HomeRoot class, or
by extending the HomeRoot class itself. We choose the latter way:

.. code-block:: python

	from solute.epfl.components import Box, Form
	
	class HomeRoot(epfl.components.CardinalLayout):
	    def init_struct(self):
	        self.node_list.extend([Box(title='My first box', node_list=[Form(cid='my_first_form')])])

We have now added a Box to the page that contains an empty form.

Now it's time to fill the form with live. We add form components to the form by extending its node_list:


.. code-block:: python

    from solute.epfl.components import TextInput, Textarea, Button

    class HomeRoot(epfl.components.CardinalLayout):

	    def init_struct(self):
	        self.node_list.extend([Box(title='Edit note',
	                                   node_list=[Form(cid='note_form', node_list=[
	                                       TextInput(label='Title',
	                                              name='title',
	                                              default='Insert a title here!'),
	                                       Textarea(label='Text',
	                                                  name='text'),
	                                       Button(value='Submit',
	                                                event_name='submit')])])])

If you take a look at the rendered page now, you can already see the form with its fields and the submit button. Neat!

Note that you can already experience the server-side state that EPFL provides: If you enter text in the form and click your 
browser's refresh button, the values of the form are kept.

As a next step, we want to handle the event when the user clicks on the submit button. You can add event handling methods to any component.
Ultimatively, we want to handle this event on our Form, since we have to react on the event and create a new note with the values of the form's fields.

Currently, the event when clicking the button is bubbled up the form. Neither the button nor the form provide an event currently, so let's add
event handling functionality to the form.
The easiest way to handle this event is by using an inherited class from Form: 

.. code-block:: python

    class NoteForm(Form):
	
        node_list = [Text(label='Title',
                            name='title',
                            default='Insert a title here!'),
                     Textarea(label='Text',
                                name='text'),
                     Button(value='Submit',
                              event_name='submit')]
                              
	class HomeRoot(epfl.components.CardinalLayout):
	
	    def init_struct(self):
	        self.node_list.extend([Box(title='Edit note',
	                                   node_list=[NoteForm(cid = 'note_form')])])

Nothing has changed so far, we have just moved the form to our own subclass from Form.

We now add the event handling method to the form. Since the button is instanciated with the value "submit"
of its attribute "event_name", epfl expects a method "handle_submit" to call for event handling. We provide this
method in our FirstFormClass:

.. code-block:: python

	class NoteForm(Form):
	
	    ...
	
	    def handle_submit(self):
	        if not self.validate():
	            self.page.show_fading_message('An error occurred in validating the form!', 'error')
	            return
	        print self.get_values()

What happens in handle_submit()? First, the form is validated. If validation fails (both input fields are mandatory, so validation fails
if a field is empty), an error message is displayed on the page. If validation succeeds, the form values are printed on the server console.

Next, we need to do something with the actual data that comes from the form. Enter ModelBase.
All classes inheriting from ModelBase serve as a kind of interface between the data layer (e.g. database connectors etc), and the view
(i.e. the epfl components). Since we don't want to use a full-blown database in this tutorial, we will use the ModelBase to simple implement 
an in-memory storage of our notes data.

We first create our class MyModel that will serve for storing, loading and removing notes, and insert the class to our page so it is accessible later:

.. code-block:: python

	from solute.epfl.core.epflassets import ModelBase
	
	class NoteModel(ModelBase):
	    pass
	
	@view_config(route_name='home')
	class HomePage(epfl.Page):
	    root_node = HomeRoot(
	    	constrained=True, node_list=[NavLayout(slot='north', title='Demo Notes App')])
	    model = NoteModel

In order to have all data management methods at hand that are needed in this tutorial, we implement the complete functionality of MyModel straight away.  

.. code-block:: python

	class NoteModel(ModelBase):
	    data_store = {'_id_counter': 1}
	
	    def add_note(self, note):
	        note['id'] = self.data_store['_id_counter']
	        self.data_store['_id_counter'] += 1
	        self.data_store.setdefault('notes', []).append(note)
	
	    def remove_note(self, note_id):
	        self.data_store['notes'] = [note for note in self.data_store['notes'] if note['id'] != note_id]
	
	    def get_note(self, note_id):
	        return [note for note in self.data_store['notes'] if note['id'] == note_id][0]
	
	    def set_note(self, note_id, value):
	        self.get_note(note_id).update(value)
	
	    def load_notes(self, calling_component, *args, **kwargs):
	        return self.data_store.get('notes', [])

The NoteModel class stores notes as dict objects in an in-memory list and provides methods for adding, removing, getting and updating a notes,
as well as for obtaining the complete list of notes.

Every component has access to the page it is located in by using self.page. Hence, every component has access to the NoteModel as well.
We can now call add_note() on the model in the handle_submit method of our form: 

.. code-block:: python

	def handle_submit(self):
	    if not self.validate():
	        self.page.show_fading_message('An error occurred in validating the form!', 'error')
	    values = self.get_values()
	    self.page.model.add_note({'title': values['title'],
	                              'text': values['text']})

The note is now persisted in memory. Ok, but how can we display it? Let's add a component that displays all created notes in a list.

This component will use a different way to retrieve its data values: Up to now, we directly set and read component attributes to handle component data.
For example, label, name and default value of the note form fields have been set in the constructor of the corresponding TextInput and Textarea classes.
While this is perfect for small amount of data or static data structures, it is not suited for complex data access operations.
Instead, we will use the get_data attribute, which enables us to create components dynamically based on the data its parent component receives.

Lets start by adding a simple Box below or "Edit note" box:

.. code-block:: python

	from solute.epfl.core.epflcomponentbase import ComponentBase

	class HomeRoot(epfl.components.CardinalLayout):
	
	    def init_struct(self):
	        ...
	        self.node_list.append(Box(cid='notes_list',
	                                   title='My notes',
	                                   default_child_cls=ComponentBase(),
	                                   get_data='notes'))

We have provided three new attributes for this Box: the cid is used to access the component later, get_data="notes" tells the component to use a method load_notes() on the model to obtain the data,
and default_child_cls is used to tell the component which child to create for rendering each tem of the list that load_notes() returned.

Currently, we use an empty ComponentBase object, the basic component provided by EPFL which currently does nothing.
However, with two more little tools, we can easily make this component smart enough to display its note data:

.. code-block:: python

	class HomeRoot(epfl.components.CardinalLayout):

	    def init_struct(self):
	        ...
	        self.node_list.append(Box(cid='notes_list',
	                                   title='My notes',
	                                   default_child_cls=ComponentBase(template_name='epfl_pyramid_barebone:templates/note.html'),
	                                   data_interface={'id': None,
	                                                   'text': None,
	                                                   'title': None},
	                                   get_data='notes'))

We added the data_interface dict to the box that defines the fields which are available on a date object for each child.
And for the child, we set the path to the template which will be used to render the child component's contents. To make that work,
we have to put the template under demo_app/epf_pyramid_barebone/template/note.py and fill it with the following contents:

.. code-block:: jinja

	<div epflid="{{ compo.cid }}">
	    <h2>{{ compo.title }} ({{ compo.id }})</h2>
	    <pre>
	        {{ compo.text }}
	    </pre>
	</div>
	
All we have done here is that we added a div with the epflid attribute set (this should always be done for the outermost html element of the component), and
added a h2 and pre block to this div which we fill with title and id as well as with the text attribute of the component.
These attributes (id, title, and text) are set by the get_data method with the note data, and we can directly access it within the jinja template,
where the component instance is available as the compo variable.

In order to have the "My notes" box automatically refreshed when a new note is added, we have to trigger a redraw() of the component in the
event where the note is added: 

.. code-block:: python

	class NoteForm(Form):
	    ...
	
	    def handle_submit(self):
	        ...
	        self.page.notes_list.redraw()

If you try the code now, you will see that every creation of a new note leads to a corresponding block in the "My notes" box displaying the component information!

What's next? We can easily create another component that serves as a left-hand menu which also displays the created notes (for example, to provide links to a
different view that displays a note in detail). This only takes 8 lines of code: We extend the node_list of our root component:

.. code-block:: python

	from solute.epfl.components import LinkListLayout

	class HomeRoot(epfl.components.CardinalLayout):

	    def init_struct(self):
	        ...
	        self.node_list.append(LinkListLayout(cid='notes_link_list',
	                                              get_data='notes',
	                                              auto_update_children=True,
	                                              show_pagination=False,
	                                              show_search=False,
	                                              node_list=[ComponentBase(url='/', text='Home')],
	                                              data_interface={'id': None,
	                                                              'url': 'note?id={id}',
	                                                              'text': 'title'},
	                                              slot='west'))

We used the predefined LinkListLayout component that renders its children as links.
For displaying the data, we bind the component again to notes with get_data, and set the predefined text attribute of the link to the title attribute
of the note data struct.

The list also expects an URL attribute. Here, we construct the target url with the ID of the note as parameter, which we can access with {id} inside the string.
Of course the route for the target URL is missing, but we don't care about those links right now.

Again, we have to manually trigger a redraw of this component when a new notes is added:

.. code-block:: python

	class NoteForm(Form):
	    ...
	
	    def handle_submit(self):
	        ...
	        self.page.notes_link_list.redraw()

Next, we want to use the note form not only for creating new notes, but also for editing existing notes.
First, how do we want to edit notes? Well, lets just provide an edit button in our list of notes.
Currently, our notes list containes of basic ComponentBase components which we have directly defined as default_child_cls of our notes list box.
Since these notes list children ares getting more complex now, we move the child component class to its own subclass of Box:   

.. code-block:: python

	class NoteBox(Box):
	    data_interface = {'id': None,
	                      'text': None,
	                      'title': None}
	
	    def init_struct(self):
	        self.node_list.append(ComponentBase(template_name='epfl_pyramid_barebone:templates/note.html'))
	        self.node_list.append(Button(value='Edit this note',
	                                       event_name='edit_note'))
	
	    def handle_edit_note(self):
	        pass
	        
	    ...
	
	class HomeRoot(epfl.components.CardinalLayout):
	
	    def init_struct(self):
	        ...
	        self.node_list.append(Box(cid='notes_list',
	                               title='My notes',
	                               default_child_cls=NoteBox,
	                               data_interface={'id': None,
	                                               'text': None,
	                                               'title': None},
	                               get_data='notes'))
	        ...

Note that we have already added a button to each note display component in the note list for editing the note.
And, since we moved the component for rendering the note in the list one level deeper inside the new box NoteBox,
we have to adapt its jinja template note.html. The component now has to access id, title, and text of the note from its parent class: 

.. code-block:: jinja

	<div epflid="{{ compo.cid }}">
	    <h2>{{ compo.container_compo.title }} ({{ compo.container_compo.id }})</h2>
	    <pre>
	        {{ compo.container_compo.text }}
	    </pre>
	</div>
	
Now, we have to fill the "Edit note" form with note data once the edit button is clicked.
We first add a load_note() method on our form which fills the form with the data of an existing note:

.. code-block:: python

	class NoteForm(Form):
	
	    ...
	        
	    def load_note(self, note_id):
	        note = self.page.model.get_note(note_id)
	        self.set_value('title', note['title'])
	        self.set_value('text', note['text'])
	        self.redraw()
	        
Note that we have to call self.redraw(), otherwise the UI would not get updated when the form receives new data.

Now, we simply have to call the form's load_note() method inside the handler of the edit button in our note list box:

.. code-block:: python

	class NoteBox(Box):
	    
	    ...
	
	    def handle_edit_note(self):
	        self.page.note_form.load_note(self.id)

Let's fix an annoying glitch: Every time we click on "Submit" in the form, a new note is created.
Our app does not know if a component already exists.

To fix this, we simply have to add an attribute "id" for our form which stores the id of the currently displayed note.
If it is none, a new note is created if submit is clicked and the form contents are valid, otherwise, an existing note is updated.
And since we are there, we implement a method clean_form() which empties the form (which we also want to call upon submit()):

.. code-block:: python

	class NoteForm(Form):
	
	    node_list = ...
	    
	    compo_state = Form.compo_state + ["id"]
	    id = None
	    
	    def clean_form(self):
	        self.id = None
	        self.set_value('title', '')
	        self.set_value('text', '')
	        self.redraw()
	
	    def handle_submit(self):
	        if not self.validate():
	            self.page.show_fading_message('An error occurred in validating the form!', 'error')
	            return
	        values = self.get_values()
	        note_value = {'title': values['title'],
	                      'text': values['text']}
	        if self.id is None:
	            self.page.model.add_note(note_value)
	        else:
	            self.page.model.set_note(self.id, note_value)
	        self.clean_form()
	        
	    def load_note(self, note_id):
	        note = self.page.model.get_note(note_id)
	        self.id = note['id']
	        self.set_value('title', note['title'])
	        self.set_value('text', note['text'])
	        self.redraw()
	        
Here, we did the following:

We added an attribute "id" to NoteForm. This attribute has to be persisted in the server-side state of EPFL. Otherwise, a page refresh
would yield in the form title and text values being restored, but the id of the form's current note would not be available anymore.
We do this by adding "id" to the compo_state list, a list that is provided by the base component where all fields are stored which are persisted 
in the EPFL transaction.

We then set the id attribute when loading a note in the load_note() method, and we query the id attribute upon submit to decide whether a new note 
has to be created or an existing one has to be updated.

Finally, the clean_form() method cleans the form and is called upon handle_submit() completes. 

As a last step, we want to delete existing notes.
We can easily provide this functionality since notes are displayed in Box components in the notes list, and Box supports self-removing.
We set the corresponding attribute on NoteBox and implement the corresponding event handler method:

.. code-block:: python

	class NoteBox(Box):
	    
	    ...
	    
	    is_removable = True
	    
	    def handle_removed(self):
	        super(NoteBox, self).handle_removed()
	        if self.page.note_form.id == self.id:
	            self.page.note_form.clean_form()
	        self.page.model.remove_note(self.id)

That's it! We have implemented functionality to create, display, edit, and delete notes.
The first part of the tutorial is completed.
In the second part, we extend our notes model with notes that can contain other notes, and extend the noes list by a tree that displays nested forms.
