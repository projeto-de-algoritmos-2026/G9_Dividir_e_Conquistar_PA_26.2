function toggleLock(state) {
    isLocked = state;
    document.querySelectorAll('button').forEach(b => b.disabled = state);
}

function drawState(compareP1, compareP2, bestPair) {
    drawPoints();
    if (compareP1 && compareP2) {
        ctx.beginPath();
        ctx.moveTo(compareP1.x, compareP1.y);
        ctx.lineTo(compareP2.x, compareP2.y);
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 1;
        ctx.stroke();
    }
    if (bestPair) {
        ctx.beginPath();
        ctx.moveTo(bestPair[0].x, bestPair[0].y);
        ctx.lineTo(bestPair[1].x, bestPair[1].y);
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.stroke();
    }
}

async function animateSteps(steps) {
    let bestPair = null;
    for (const step of steps) {
        if (step.type === 'compare') {
            drawState(step.p1, step.p2, bestPair);
            await new Promise(r => setTimeout(r, 20)); // Delay da animação
        } else if (step.type === 'update') {
            bestPair = [step.p1, step.p2];
            document.getElementById('stats').innerText = `Menor Distância: ${step.dist.toFixed(2)}`;
        } else if (step.type === 'done') {
            drawState(null, null, step.best);
        }
    }
    toggleLock(false);
}

document.getElementById('btn-brute').addEventListener('click', async () => {
    if (points.length < 2) return;
    toggleLock(true);
    const res = await fetch('/solve/brute', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({points})
    });
    const data = await res.json();
    animateSteps(data.steps);
});