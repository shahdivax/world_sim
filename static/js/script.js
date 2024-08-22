document.addEventListener('DOMContentLoaded', () => {
    const output = document.getElementById('output');
    const input = document.getElementById('command-input');

    input.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            const command = input.value;
            input.value = '';

            // Display the command
            output.innerHTML += `<div><span class="prompt">world_sim> </span>${command}</div>`;

            if (command.toLowerCase() === 'reset') {
                await resetSimulator();
            } else if (command.toLowerCase() === 'exit') {
                output.innerHTML += '<div>Exiting World Simulator. Goodbye!</div>';
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
                body: JSON.stringify({ command }),
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

    // Matrix-like background effect with 'WORLD SIM'
    const canvas = document.getElementById('matrix-bg');
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const text = 'WORLD SIM';
    const fontSize = 16;
    const columns = canvas.width / fontSize;

    const rainDrops = [];

    for (let x = 0; x < columns; x++) {
        rainDrops[x] = 1;
    }

    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = 'rgba(144, 238, 144, 0.6)';  // Light green with transparency
        ctx.font = fontSize + 'px monospace';

        for (let i = 0; i < rainDrops.length; i++) {
            const character = text[Math.floor(Math.random() * text.length)];
            ctx.fillText(character, i * fontSize, rainDrops[i] * fontSize);

            if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                rainDrops[i] = 0;
            }
            rainDrops[i]++;
        }
    }

    setInterval(draw, 30);
});