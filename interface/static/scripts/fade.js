const fadeElements = document.querySelectorAll('.fade-in')

const appearOptions = {
    threshold: 0.25
}

const appearOnScroll = new IntersectionObserver( (entries, appearOnScroll) =>{
    entries.forEach(entry => {
        if (!entry.isIntersecting) {
            return
        } else {
            entry.target.classList.add('appear')
            appearOnScroll.unobserve(entry.target)
        }
    })
}, appearOptions)

fadeElements.forEach(fader => {
    appearOnScroll.observe(fader)
})