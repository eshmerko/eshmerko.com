document.addEventListener('DOMContentLoaded', function() {
    const shareContainers = document.querySelectorAll('.article-share');
    const svgIcons = {
        facebook: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#1877f2"><path d="M22.675 0H1.325C.593 0 0 .593 0 1.326V22.67C0 23.407.593 24 1.325 24H12.82v-9.292h-3.29v-3.622h3.29V8.413c0-3.26 1.993-5.032 4.902-5.032 1.392 0 2.59.104 2.94.15v3.41h-2.017c-1.58 0-1.886.752-1.886 1.852v2.429h3.775l-.492 3.622h-3.283V24h6.437C23.408 24 24 23.407 24 22.674V1.326C24 .593 23.408 0 22.675 0z"/></svg>`,
        vk: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#4680C2"><path d="M12.35 16.23c-4.745 0-7.21-3.12-7.31-8.61h2.422c.056 4.16 1.912 5.92 3.355 6.26V7.62h2.31v3.46c1.423-.153 2.91-1.776 3.41-3.46h2.31a7.607 7.607 0 0 1-3.57 4.78 7.815 7.815 0 0 1 4.02 4.83h-2.59a6.43 6.43 0 0 0-3.95-3.84v3.84h-.982z"/></svg>`,
        telegram: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 240 240"><path fill="#0088cc" d="M120 0C53.7 0 0 53.7 0 120s53.7 120 120 120 120-53.7 120-120S186.3 0 120 0zm55.4 82.4-18.6 87.7c-1.4 6.2-5.2 7.7-10.5 4.8l-29.1-21-14 13.5c-1.5 1.5-2.8 2.8-5.8 2.8l2-29.4 53.6-48.5c2.3-2 0-3.2-3.5-1.2l-66.2 41.6-28.6-8.9c-6.2-1.9-6.4-6.2 1.3-9.2l111.7-43.2c5.2-1.9 9.8 1.2 8.1 9.1z"/></svg>`,
        twitter: `<svg xmlns="http://www.w3.org/2000/svg" fill="#1DA1F2" viewBox="0 0 24 24" width="20" height="20"><path d="M23.954 4.569c-.885.392-1.83.656-2.825.775 1.014-.611 1.794-1.574 2.163-2.723-.95.564-2.005.974-3.127 1.195-.897-.956-2.178-1.555-3.594-1.555-2.717 0-4.92 2.203-4.92 4.917 0 .39.045.765.127 1.124-4.09-.205-7.719-2.165-10.148-5.144-.424.729-.666 1.576-.666 2.475 0 1.708.87 3.215 2.188 4.099-.807-.026-1.566-.248-2.228-.616v.06c0 2.385 1.693 4.374 3.946 4.827-.413.112-.849.171-1.296.171-.314 0-.615-.03-.916-.086.631 1.953 2.445 3.377 4.6 3.417-1.68 1.318-3.809 2.105-6.102 2.105-.39 0-.779-.023-1.17-.067C2.29 21.392 5.002 22.5 7.95 22.5c9.142 0 14.307-7.721 13.995-14.646.961-.695 1.8-1.562 2.46-2.561z"/></svg>`,
        whatsapp: `<svg xmlns="http://www.w3.org/2000/svg" fill="#25D366" viewBox="0 0 24 24" width="20" height="20"><path d="M20.52 3.48a11.81 11.81 0 0 0-16.7 0A11.81 11.81 0 0 0 2.1 14.13l-1.13 4.18a1 1 0 0 0 1.21 1.22l4.18-1.13a11.81 11.81 0 0 0 10.65-1.64 11.81 11.81 0 0 0 0-16.7zm-4.69 12.58c-.28.79-1.41 1.47-2.13 1.57-.55.08-1.24.11-4.07-.86A14.5 14.5 0 0 1 6.56 13c-1.4-1.92-1.67-3.58-1.78-4.15-.12-.63.3-1.36.69-1.66.28-.21.68-.3 1.09-.19.13.04.26.09.38.15l1.26.62c.33.17.56.56.6.94.05.56.11 1.1-.05 1.33-.15.22-.45.52-.66.69-.2.17-.4.34-.18.66.21.32.93 1.52 2.01 2.07 1.1.58 1.33.51 1.59.44.26-.07.84-.34.96-.66.12-.33.47-.53.79-.36.33.17 1.96.93 2.29 1.1.33.17.55.26.63.4.08.15.08.83-.2 1.62z"/></svg>`,
        linkedin: `<svg xmlns="http://www.w3.org/2000/svg" fill="#0077B5" viewBox="0 0 24 24" width="20" height="20"><path d="M20.447 20.452h-3.554v-5.569c0-1.327-.024-3.037-1.849-3.037-1.851 0-2.134 1.444-2.134 2.936v5.67h-3.554V9h3.414v1.561h.049c.476-.899 1.637-1.847 3.369-1.847 3.599 0 4.263 2.368 4.263 5.451v6.287zM5.337 7.433c-1.144 0-2.07-.926-2.07-2.07s.926-2.07 2.07-2.07 2.07.926 2.07 2.07-.926 2.07-2.07 2.07zm1.777 13.019H3.56V9h3.554v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.727v20.546C0 23.226.792 24 1.771 24h20.451C23.2 24 24 23.226 24 22.273V1.727C24 .774 23.2 0 22.225 0z"/></svg>`
    };
    
    
    shareContainers.forEach(container => {
        const originalButton = container.querySelector('.share-button');
        if (!originalButton) return;

        // Сохраняем оригинальный SVG
        const originalSVG = originalButton.innerHTML;
        
        const pageTitle = document.title;
        const pageUrl = window.location.href.split('?')[0];

        // Создаем обертку для элементов
        const wrapper = document.createElement('div');
        wrapper.className = 'share-wrapper';

        // Создаем контейнер для социальных кнопок
        const socialButtonsRow = document.createElement('div');
        socialButtonsRow.className = 'inline-social-buttons';
        socialButtonsRow.style.display = 'none';
        socialButtonsRow.style.flexDirection = 'row';       // горизонтальное направление
        socialButtonsRow.style.gap = '10px';                // отступ между кнопками
        socialButtonsRow.style.marginTop = '10px';          // отступ сверху
        socialButtonsRow.style.flexWrap = 'wrap';           // перенос при необходимости
        socialButtonsRow.style.alignItems = 'center';       // вертикальное выравнивание


        // Модифицируем оригинальную кнопку
        originalButton.classList.add('main-button');
        originalButton.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();

            if (navigator.share) {
                try {
                    await navigator.share({
                        title: pageTitle,
                        url: pageUrl
                    });
                } catch (error) {
                    if (error.name !== 'AbortError') {
                        console.error('Ошибка шаринга:', error);
                    }
                }
            } else {
                socialButtonsRow.style.display = socialButtonsRow.style.display === 'none' ? 'flex' : 'none';
            }
        });
        

        // Создаем кнопки социальных сетей
        const socialNetworks = [
            { 
                name: 'FB', 
                title: 'Facebook', 
                class: 'facebook-btn', 
                url: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(pageUrl)}`
            },
            { 
                name: 'VK', 
                title: 'ВКонтакте', 
                class: 'vk-btn', 
                url: `https://vk.com/share.php?url=${encodeURIComponent(pageUrl)}`
            },
            { 
                name: 'TG', 
                title: 'Telegram', 
                class: 'telegram-btn', 
                url: `https://t.me/share/url?url=${encodeURIComponent(pageUrl)}`
            },
            { 
                name: 'TW', 
                title: 'Twitter', 
                class: 'twitter-btn', 
                url: `https://twitter.com/intent/tweet?url=${encodeURIComponent(pageUrl)}`
            },
            { 
                name: 'WA', 
                title: 'WhatsApp', 
                class: 'whatsapp-btn', 
                url: `https://api.whatsapp.com/send?text=${encodeURIComponent(pageUrl)}`
            },
            { 
                name: 'LN', 
                title: 'LinkedIn', 
                class: 'linkedin-btn', 
                url: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(pageUrl)}`
            }
        ];


        socialNetworks.forEach(network => {
            const button = document.createElement('button');
            button.className = `social-btn ${network.class}`;
            button.title = network.title;
            button.innerHTML = svgIcons[network.class.replace('-btn', '')] || `<span>${network.name}</span>`;
            
            button.addEventListener('click', () => {
                window.open(network.url, '_blank', 'noopener,noreferrer');
            });
            
            socialButtonsRow.appendChild(button);
        });

        // Добавляем элементы в DOM
        wrapper.appendChild(originalButton);
        wrapper.appendChild(socialButtonsRow);
        container.appendChild(wrapper);
    });

    // Обработчик клика вне области
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.share-wrapper')) {
            document.querySelectorAll('.inline-social-buttons').forEach(buttons => {
                buttons.style.display = 'none';
            });
        }
    });
});