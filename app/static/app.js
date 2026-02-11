const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 }
);

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

const counters = document.querySelectorAll('[data-counter]');
counters.forEach((counter) => {
  const target = Number(counter.dataset.counter || 0);
  let current = 0;
  const step = Math.max(1, Math.ceil(target / 30));
  const timer = setInterval(() => {
    current += step;
    if (current >= target) {
      counter.textContent = target.toString();
      clearInterval(timer);
      return;
    }
    counter.textContent = current.toString();
  }, 30);
});

document.querySelectorAll('.tilt').forEach((card) => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const rotateX = -((y / rect.height) - 0.5) * 8;
    const rotateY = ((x / rect.width) - 0.5) * 8;
    card.style.transform = `perspective(700px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = 'perspective(700px) rotateX(0) rotateY(0)';
  });
});
