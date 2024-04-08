window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        transitionToDashboardPage: async function (n_clicks_timestamp) {
            console.log(`Callback triggered with n_clicks_timestamp: ${n_clicks_timestamp}`);
            if (n_clicks_timestamp !== undefined) {
                console.log('Button has been clicked, transitioning to new page...');
                await new Promise(r => setTimeout(r, 400));
                console.log('Transition complete, navigating to /dashboard');
                return '/dashboard';
            } else {
                console.log('Button has not been clicked or callback triggered by initial render (n_clicks_timestamp is undefined). No transition will occur.');
            }
            return window.dash_clientside.no_update;
        },
        transitionToAnalysisPage: async function (n_clicks_timestamp) {
            console.log(`Callback triggered with n_clicks_timestamp: ${n_clicks_timestamp}`);
            if (n_clicks_timestamp !== undefined) {
                console.log('Button has been clicked, transitioning to new page...');
                await new Promise(r => setTimeout(r, 400));
                console.log('Transition complete, navigating to /dashboard');
                return '/analysis';
            } else {
                console.log('Button has not been clicked or callback triggered by initial render (n_clicks_timestamp is undefined). No transition will occur.');
            }
            return window.dash_clientside.no_update;
        },

        setupCustomScroll: function (children) {
            // This function will run every time the container's children are updated.
            // Ensure it's the right condition to add the event listener, for example,
            // by checking if the container exists now in the DOM.
            const container = document.querySelector('#analysis-page-scroll-container');
            console.log('Setting up custom scroll event listener...')
            if (container) {
                console.log('Container found, setting up custom scroll event listener...')
                // If the container exists, attach the custom scrolling event listener.
                //const items = container.querySelectorAll('.scroll-item');
                const scrollSpeed = 2; // Adjust this value to control the scroll speed

                container.addEventListener('wheel', (event) => {
                    event.preventDefault();
                    const delta = event.deltaY * scrollSpeed; // Multiply the wheel delta by the speed factor
                    // however, if mouse is in '.zoomable' element (its children)
                    // then do not scroll
                    //console.log(event.target)
                    if (!event.target.closest('.zoomable')) {
                        container.scrollBy({
                            top: delta,
                            behavior: 'auto' // Use 'auto' for instantaneous scroll, which we'll animate manually
                        });
                    }

                    // Set up the Intersection Observer
                    const observerOptions = {
                        root: container,
                        threshold: 0.5, // Adjust as needed, 0.5 means 50% of the item is visible
                    };
                    const observerCallback = (entries, observer) => {
                        entries.forEach(entry => {
                            const children = entry.target.querySelectorAll('.scroll-item-animate');
                            // Get class name that match the pattern 'need-animate-*' and only return the latter * part
                            //Array.from(child).find(className => className.startsWith('need-animate-')).replace('need-', '');
                            if (entry.isIntersecting) {
                                entry.target.classList.remove('opacity-0');
                                entry.target.classList.add('opacity-100');
                                // Add the 'animate-slide-in-x', 'animate-700', and 'animate-delay-400' classes
                                // along with the specific animation classes from the pattern
                                // get all children with class 'scroll-item-animate'
                                children.forEach((child, index) => {
                                    const animationClasses = Array.from(child.classList).filter(className => className.startsWith('need-')).map(className => className.replace('need-', ''));
                                    child.classList.add(
                                        ...animationClasses
                                    );
                                });
                                //observer.unobserve(entry.target);
                                //console.log('Unobserving item...')
                            }
                            else {
                                // opacity of entry.target to 0 by transition
                                entry.target.classList.remove('opacity-100');
                                entry.target.classList.add('opacity-0');
                                // Reset the animation by removing all the classes
                                children.forEach((child, index) => {
                                    // if 'repeat-animation' is in classList, then it indicates the animation classes should be removed when leave the viewport
                                    if (child.classList.contains('repeat-animation')) {
                                        const animationClasses = Array.from(child.classList).filter(className => className.startsWith('need-')).map(className => className.replace('need-', ''));
                                        child.classList.remove(
                                            ...animationClasses
                                        );
                                    }
                                });
                            }
                        });
                    };

                    const observer = new IntersectionObserver(observerCallback, observerOptions);

                    // Observe each scroll item
                    const items = container.querySelectorAll('.scroll-item-container');
                    //console.log('Observing items...', items)
                    items.forEach(item => {
                        // if not already observed
                        if (!item.classList.contains('observed')) {
                            item.classList.add('observed');
                            observer.observe(item);
                        }
                    });

                });
                return window.dash_clientside.no_update;
            }

            // Return false or some other dummy value if the container is not yet available.
            return window.dash_clientside.no_update;
        }
    }
});