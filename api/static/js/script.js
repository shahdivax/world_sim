document.addEventListener('DOMContentLoaded', () => {
    const output = document.getElementById('output');
    const input = document.getElementById('command-input');
    const modelSelect = document.getElementById('model-select');

    modelSelect.addEventListener('change', async () => {
        const selectedModel = modelSelect.value;
        await setModel(selectedModel);
    });

    input.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            const command = input.value;
            input.value = '';

            // Display the command
            output.innerHTML += `<div><span class="prompt">world_sim> </span>${command}</div>`;

            if (command.toLowerCase() === 'reset') {
                await resetSimulator();
            } else if (command.toLowerCase() === 'exit') {
                window.location.href = '/home';
            } else {
                await executeCommand(command);
            }

            // Scroll to bottom
            output.scrollTop = output.scrollHeight;
        }
    });

    async function executeCommand(command) {
        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command, model: modelSelect.value }),
            });

            const data = await response.json();
            output.innerHTML += data.response;
        } catch (error) {
            console.error('Error:', error);
            output.innerHTML += '<div>An error occurred while processing your command.</div>';
        }
    }

    async function resetSimulator() {
        try {
            const response = await fetch('/reset', {
                method: 'POST',
            });

            const data = await response.json();
            output.innerHTML = data.response;
        } catch (error) {
            console.error('Error:', error);
            output.innerHTML += '<div>An error occurred while resetting the simulator.</div>';
        }
    }

    async function setModel(model) {
        try {
            const response = await fetch('/set_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ model }),
            });

            const data = await response.json();
            if (data.success) {
                output.innerHTML += `<div>Model changed to: ${data.model}</div>`;
            } else {
                output.innerHTML += `<div>Error changing model: ${data.error}</div>`;
            }
        } catch (error) {
            console.error('Error:', error);
            output.innerHTML += '<div>An error occurred while changing the model.</div>';
        }
    }

});