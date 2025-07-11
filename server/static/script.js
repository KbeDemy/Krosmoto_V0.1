function startMusic() {
    const audio = document.getElementById('bg-music');
    audio.volume = 0.5;
    audio.play().catch(err => {
        console.error("Autoplay geblokkeerd:", err);
    });
}

document.addEventListener('click', () => {
    startMusic();
}, { once: true });

function createTicksWithLabels(svgGroup, maxTicks, radiusOuter, radiusInner, radiusLabel, maxValue, unit = '') {
    const centerX = 100, centerY = 100;
    const startAngle = -180, totalAngle = 180;

    for (let i = 0; i <= maxTicks; i++) {
        const angleDeg = startAngle + (totalAngle / maxTicks) * i;
        const angleRad = angleDeg * (Math.PI / 180);

        const x1 = centerX + radiusOuter * Math.cos(angleRad);
        const y1 = centerY + radiusOuter * Math.sin(angleRad);
        const x2 = centerX + radiusInner * Math.cos(angleRad);
        const y2 = centerY + radiusInner * Math.sin(angleRad);

        const tick = document.createElementNS("http://www.w3.org/2000/svg", "line");
        tick.setAttribute("x1", x1);
        tick.setAttribute("y1", y1);
        tick.setAttribute("x2", x2);
        tick.setAttribute("y2", y2);
        tick.setAttribute("class", "tick");
        svgGroup.appendChild(tick);

        const lx = centerX + radiusLabel * Math.cos(angleRad);
        const ly = centerY + radiusLabel * Math.sin(angleRad);

        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", lx);
        label.setAttribute("y", ly + 5);
        label.setAttribute("text-anchor", "middle");
        label.setAttribute("class", "tick-label");
        label.textContent = Math.round((maxValue / maxTicks) * i) + unit;
        svgGroup.appendChild(label);
    }
}

const ticksSpeedGroup = document.getElementById('ticks-speed');
createTicksWithLabels(ticksSpeedGroup, 8, 90, 80, 105, 80);

const ticksRpmGroup = document.getElementById('ticks-rpm');
createTicksWithLabels(ticksRpmGroup, 8, 90, 80, 105, 4000);

let currentSpeed = 0;
function setSpeedNeedle(speed) {
    const maxSpeed = 80;
    const maxAngle = 180;
    const speedToAngle = s => (s / maxSpeed) * maxAngle - 90;
    const needle = document.getElementById("needle-speed");
    const speedText = document.getElementById("speed-text");

    const startAngle = speedToAngle(currentSpeed);
    const endAngle = speedToAngle(Math.min(speed, maxSpeed));
    const duration = 800, frameRate = 60, totalFrames = duration / (1000 / frameRate);
    let frame = 0;

    function animate() {
        frame++;
        const progress = frame / totalFrames;
        const ease = progress < 0.5 ? 4 * progress ** 3 : 1 - ((-2 * progress + 2) ** 3) / 2;
        const angle = startAngle + (endAngle - startAngle) * ease;
        needle.setAttribute("transform", `rotate(${angle} 100 100)`);
        speedText.textContent = Math.round(currentSpeed + (speed - currentSpeed) * ease) + " km/h";
        if (frame < totalFrames) requestAnimationFrame(animate);
        else currentSpeed = Math.min(speed, maxSpeed);
    }
    animate();
}

let currentRPM = 0;
function setRPMNeedle(rpm) {
    const maxRPM = 4000;
    const maxAngle = 180;
    const rpmToAngle = r => (r / maxRPM) * maxAngle - 90;
    const needle = document.getElementById("needle-rpm");
    const rpmText = document.getElementById("rpm-text");

    const startAngle = rpmToAngle(currentRPM);
    const endAngle = rpmToAngle(Math.min(rpm, maxRPM));
    const duration = 800, frameRate = 60, totalFrames = duration / (1000 / frameRate);
    let frame = 0;

    function animate() {
        frame++;
        const progress = frame / totalFrames;
        const ease = progress < 0.5 ? 4 * progress ** 3 : 1 - ((-2 * progress + 2) ** 3) / 2;
        const angle = startAngle + (endAngle - startAngle) * ease;
        needle.setAttribute("transform", `rotate(${angle} 100 100)`);
        rpmText.textContent = Math.round(currentRPM + (rpm - currentRPM) * ease) + " RPM";
        if (frame < totalFrames) requestAnimationFrame(animate);
        else currentRPM = Math.min(rpm, maxRPM);
    }
    animate();
}

setInterval(() => {
    const speedVal = Math.floor(Math.random() * 81);
    const rpmVal = Math.floor(Math.random() * 4001);
    setSpeedNeedle(speedVal);
    setRPMNeedle(rpmVal);
}, 2000);
