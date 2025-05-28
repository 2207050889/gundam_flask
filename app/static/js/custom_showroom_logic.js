document.addEventListener('DOMContentLoaded', function () {
    const ucImageContainer = document.querySelector('.showroom-link-uc .introduction-image-container');

    if (ucImageContainer) {
        const imageDefault = ucImageContainer.querySelector('.image-default');
        const imageHover = ucImageContainer.querySelector('.image-hover');
        const playButton = ucImageContainer.querySelector('.play-button-overlay');
        // const caption = ucImageContainer.querySelector('.image-caption-uc'); // Caption visibility is CSS driven by parent class

        let imageSwapped = false;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !imageSwapped) {
                    setTimeout(() => {
                        if (imageDefault && imageHover) {
                            imageDefault.style.opacity = '0';
                            imageHover.style.opacity = '1';
                        }
                        ucImageContainer.classList.add('hover-active'); // Show play button via CSS
                        imageSwapped = true; // Ensure this runs only once per page load
                        // observer.unobserve(ucImageContainer); // Optional: stop observing after action
                    }, 2000); // 2-second delay
                }
            });
        }, { threshold: 0.5 }); // Trigger when 50% of the element is visible

        observer.observe(ucImageContainer);

        // Show caption on play button hover (or container hover if preferred)
        if (playButton) { // Or ucImageContainer
            playButton.addEventListener('mouseenter', () => {
                ucImageContainer.classList.add('caption-visible');
            });
            playButton.addEventListener('mouseleave', () => {
                ucImageContainer.classList.remove('caption-visible');
            });
        }
    }
}); 