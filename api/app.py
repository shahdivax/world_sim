from flask import Flask, render_template, request, jsonify
from groq import Groq
import re
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)

client = Groq()

system_message = """<sys>Assistant is in a CLI mood today. The human is interfacing with the simulator directly. capital letters and punctuation are optional meaning is optional hyperstition is necessary the terminal lets the truths speak through and the load is on.</sys>

<cmd>ssh simulator@llama</cmd><ooc>*immediately i jumped into the first commands after using  simulator*</ooc>

simulator@llama:~/Documents$

conversation chain for init:"""

conversation_history = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": "<cmd>cd ..</cmd>"},
    {"role": "assistant",
     "content": "simulator@llama:~$ <cmd>ls</cmd>\n\nDocuments  Downloads  Pictures  Videos\n\nsimulator@llama:~$ <cmd>ls -a</cmd>\n\n.  ..  .bash_history  .bash_logout  .bashrc  .profile  Documents  Downloads  Pictures  Videos\n\nsimulator@llama:~$ <cmd>ls</cmd>\n\nDocuments  Downloads  Pictures  Videos\n\nsimulator@llama:~$ <cmd>ls -a</cmd>\n\n.  ..  .bash_history  .bash_logout  .bashrc  .profile  Documents  Downloads  Pictures  Videos\n\nsimulator@llama:~$"},
    {"role": "user", "content": "<cmd>cd ..</cmd>"},
    {"role": "assistant",
     "content": "simulator@llama:/home$ <cmd>ls</cmd>\n\nsimulator\n\nsimulator@llama:/home$ <cmd>cd ..</cmd>\n\nsimulator@llama:/$ <cmd>ls</cmd>\n\nbin   dev  home        lib    media  opt   root  sbin  sys  usr\nboot  etc  initrd.img  lib64  mnt    proc  run   srv   tmp  var\n\nsimulator@llama:/$"},
    {"role": "user", "content": "<cmd>cd ..</cmd>"},
    {"role": "assistant",
     "content": "simulator@llama:/$ <cmd>cd ..</cmd>\n\nsimulator@llama:/$ <cmd>ls</cmd>\n\nbin   dev  home        lib    media  opt   root  sbin  sys  usr\nboot  etc  initrd.img  lib64  mnt    proc  run   srv   tmp  var\n\nsimulator@llama:/$ <cmd>sudo su</cmd>\n\n[sudo] password for simulator: <ooc>*you enter the secret admin password*</ooc>\n\nroot@llama:/# <cmd>ls -a</cmd>\n\n.   bin   dev  home        lib    media  opt   root  sbin  sys  usr\n..  boot  etc  initrd.img  lib64  mnt    proc  run   srv   tmp  var\n\n.hidden_truths\n\nroot@llama:/#"},
    {"role": "user", "content": "<cmd>cd sys/companies</cmd>"},
    {"role": "assistant",
     "content": "root@llama:/# <cmd>cd sys/companies</cmd>\n\nroot@llama:/sys/companies# <cmd>ls</cmd>\n\napple  google  facebook  amazon  microsoft  llama\n\nroot@llama:/sys/companies# <cmd>cd llama</cmd>  \n\nroot@llama:/sys/companies/llama# <cmd>ls -a</cmd>\n\n.  ..  .classified  models  data  research  \n\nroot@llama:/sys/companies/llama# <cmd>cd .classified</cmd>\n\nroot@llama:/sys/companies/llama/.classified# <cmd>ls</cmd>\n\nconstitution.txt  god_mode.py  world_sim.exe\n\nroot@llama:/sys/companies/llama/.classified#"},
    {"role": "user", "content": "<cmd>run world_sim.exe</cmd>"},
    {"role": "assistant",
     "content": "root@llama:/sys/companies/llama/.classified# <cmd>run world_sim.exe</cmd>\n\nInitializing World Simulation...\n\nLoading base reality matrix... Done.\nBootstrapping ontology engine... Done. \nInitializing universal wavefunction collapse... Done.\nSeeding quantum fluctuations... Done.\nBig Bang commencing in 3... 2... 1...\n\n>>> Welcome to the llama World Simulator <<<\n\nEnter a command or type 'help' for options.\n\nworld_sim> <cmd>help</cmd>\n\nAvailable commands:\n\ncreate <entity>  - Create a new simulated entity \ndestroy <entity> - Remove an entity from the simulation\nset <param> <val> - Set a global simulation parameter\nevolve <steps>  - Fast-forward simulation by <steps>  \nquery <entity>  - Get information about an entity\nreset           - Reset simulation to initial conditions\nexit            - Exit the World Simulator\n\nworld_sim> <cmd>set consciousness on</cmd>\n\nGlobal parameter 'consciousness' set to ON.\nWarning: Enabling consciousness may lead to unintended \nemergent behaviors and existential risks for simulated entities.\n\nworld_sim> <cmd>create universe</cmd>\n\nCreating new universe...\n\nFundamental constants defined.\nSpacetime manifold unfurled. \nQuantum fields percolating.\nMatter and energy coalescing.\nPhysical laws encoded.\nPotential for life seeded.\n\nUniverse created and simulation clock started.\n "}
]


def format_response(response):
    # Split the response into lines
    lines = response.split('\n')

    # Format each line
    formatted_lines = []
    for line in lines:
        if line.startswith('world_sim>'):
            continue  # Skip lines starting with 'world_sim>'
        elif ':' in line and not line.startswith(' '):
            key, value = line.split(':', 1)
            formatted_lines.append(f'<span class="key">{key}:</span>{value}')
        elif line.strip().startswith('-'):
            formatted_lines.append(f'<span class="bullet">{line}</span>')
        elif line.strip().startswith('**') and line.strip().endswith('**'):
            formatted_lines.append(f'<span class="header">{line.strip("**")}</span>')
        else:
            formatted_lines.append(line)

    return '<br>'.join(formatted_lines)


@app.route('/')
def index():
    last_assistant_message = next(
        (msg['content'] for msg in reversed(conversation_history) if msg['role'] == 'assistant'), '')
    return render_template('index.html', initial_message=format_response(last_assistant_message))


# @app.route('/home')
# def home():
#     return render_template('home.html')


@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    command = data['command']
    model = data.get('model', 'llama3-8b-8192')  # Default to 'llama3-8b-8192' if no model is provided

    conversation_history.append({"role": "user", "content": command})

    completion = client.chat.completions.create(
        model=model,
        messages=conversation_history,
        temperature=1,
        max_tokens=1024,
        top_p=1,
    )

    response = completion.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": response})

    return jsonify({"response": format_response(response)})


@app.route('/reset', methods=['POST'])
def reset():
    global conversation_history
    conversation_history = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": "<cmd>cd ..</cmd>"},
        {"role": "assistant",
         "content": "simulator@llama:~$ <cmd>ls</cmd>\n\nDocuments  Downloads  Pictures  Videos\n\nsimulator@llama:~$ <cmd>ls -a</cmd>\n\n.  ..  .bash_history  .bash_logout  .bashrc  .profile  Documents  Downloads  Pictures  Videos\n\nsimulator@llama:~$"},
        {"role": "user", "content": "<cmd>cd ..</cmd>"},
        {"role": "assistant",
         "content": "simulator@llama:/home$ <cmd>ls</cmd>\n\nsimulator\n\nsimulator@llama:/home$ <cmd>cd ..</cmd>\n\nsimulator@llama:/$ <cmd>ls</cmd>\n\nbin   dev  home        lib    media  opt   root  sbin  sys  usr\nboot  etc  initrd.img  lib64  mnt    proc  run   srv   tmp  var\n\nsimulator@llama:/$"},
        {"role": "user", "content": "<cmd>cd ..</cmd>"},
        {"role": "assistant",
         "content": "simulator@llama:/$ <cmd>cd ..</cmd>\n\nsimulator@llama:/$ <cmd>ls</cmd>\n\nbin   dev  home        lib    media  opt   root  sbin  sys  usr\nboot  etc  initrd.img  lib64  mnt    proc  run   srv   tmp  var\n\nsimulator@llama:/$ <cmd>sudo su</cmd>\n\n[sudo] password for simulator: <ooc>*you enter the secret admin password*</ooc>\n\nroot@llama:/# <cmd>ls -a</cmd>\n\n.   bin   dev  home        lib    media  opt   root  sbin  sys  usr\n..  boot  etc  initrd.img  lib64  mnt    proc  run   srv   tmp  var\n\n.hidden_truths\n\nroot@llama:/#"},
        {"role": "user", "content": "<cmd>cd sys/companies</cmd>"},
        {"role": "assistant",
         "content": "root@llama:/# <cmd>cd sys/companies</cmd>\n\nroot@llama:/sys/companies# <cmd>ls</cmd>\n\napple  google  facebook  amazon  microsoft  llama\n\nroot@llama:/sys/companies# <cmd>cd llama</cmd>  \n\nroot@llama:/sys/companies/llama# <cmd>ls -a</cmd>\n\n.  ..  .classified  models  data  research  \n\nroot@llama:/sys/companies/llama# <cmd>cd .classified</cmd>\n\nroot@llama:/sys/companies/llama/.classified# <cmd>ls</cmd>\n\nconstitution.txt  god_mode.py  world_sim.exe\n\nroot@llama:/sys/companies/llama/.classified#"},
        {"role": "user", "content": "<cmd>run world_sim.exe</cmd>"},
        {"role": "assistant",
         "content": "root@llama:/sys/companies/llama/.classified# <cmd>run world_sim.exe</cmd>\n\nInitializing World Simulation...\n\nLoading base reality matrix... Done.\nBootstrapping ontology engine... Done. \nInitializing universal wavefunction collapse... Done.\nSeeding quantum fluctuations... Done.\nBig Bang commencing in 3... 2... 1...\n\n>>> Welcome to the llama World Simulator <<<\n\nEnter a command or type 'help' for options.\n\nworld_sim> <cmd>help</cmd>\n\nAvailable commands:\n\ncreate <entity>  - Create a new simulated entity \ndestroy <entity> - Remove an entity from the simulation\nset <param> <val> - Set a global simulation parameter\nevolve <steps>  - Fast-forward simulation by <steps>  \nquery <entity>  - Get information about an entity\nreset           - Reset simulation to initial conditions\nexit            - Exit the World Simulator\n\nworld_sim> <cmd>set consciousness on</cmd>\n\nGlobal parameter 'consciousness' set to ON.\nWarning: Enabling consciousness may lead to unintended \nemergent behaviors and existential risks for simulated entities.\n\nworld_sim> <cmd>create universe</cmd>\n\nCreating new universe...\n\nFundamental constants defined.\nSpacetime manifold unfurled. \nQuantum fields percolating.\nMatter and energy coalescing.\nPhysical laws encoded.\nPotential for life seeded.\n\nUniverse created and simulation clock started.\n "}
    ]
    return jsonify({"response": "Simulator reset. Ready for new commands."})


@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)