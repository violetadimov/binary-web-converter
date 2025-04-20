function kaelyraActivate() {
  const orb = document.querySelector('.kaelyra-orb');
  const dialogue = document.getElementById('kaelyra-dialogue')
  const modal = document.getElementById('kaelyra-modal');

  orb.style.boxShadow = '0 0 30px 10px rgba(255,255,255,0.9)';
  orb.style.transform = 'scale(1.2)';

  const messages = [
      "I'm listening...What shall we create?",
      "Sketching a structure in my mind...",
      "Let's build something exceptional.",
      "Show me your vision. I'll translate it."
  ]
  const message = messages[Math.floor(Math.random() * messages.length)];

  dialogue.innerText = message;
  dialogue.style.opacity = 1;

  modal.style.display = "block";

  setTimeout(() => {
    orb.style.boxShadow = '';
    orb.style.transform = '';
    // future: trigger command generation, AI interaction, or modal
    console.log("Kaelyra is listening...");
  }, 800);

  setTimeout(() => {
    dialogue.style.opacity = 0;
  }, 4000);
}

function submitKaelyraCommand() {
  const input = document.getElementById('kaelyra-input').value.trim();
  const modal = document.getElementById('kaelyra-input');
  const dialogue = document.getElementById('kaelyra-dialogue');

  if (input.includes("create a website")) {
    //Simulated response - replace this with real AU call later
    dialogue.innerText = "Understood. Building a site layout now.";
  } else if (input.includes("brighten skin")) {
    dialogue.innerText = "Fetching Glowrestore routine...";
  } else {
    dialogue.innerText = `${input} received. Building your vision...`;

    //dialogue.style.opacity = 1;

    //hide modal
    modal.style.display = "none";
    document.getElementById('kaelyra-input').value = '';

    setTimeout(() => {
      dialogue.style.opacity = 0;
    }, 4000);
  }
}

const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
recognition.onresult = function(event) {
  const transcript = event.results[0][0].transcript;
  document.getElementById('kaelyra-input').value = transcript;
};