// Pulpe v0.1 client script

var current_search = ''
var current_page = 0

search = () => {
    // Perform a search on videos

    if (!current_page) {
        grid = $('#grid')
        grid.empty()
    }

    $.getJSON(`/search?query=${current_search}&page=${current_page}`, els => {
        $(els).each((i, el) => {

            video = el.replace('_', '-')
                      .replace('.mp4', '')
                      .split('-')

            agent = video[0].charAt(0).toUpperCase() + video[0].slice(1)

            grid.append(`
            <div class="video" data-name="${agent} (${video[1].toUpperCase()})">
                <video class="video-js vjs-fill" controls>
                    <source src="/get/${el}">
                </video>
            </div>`)
        })
    })
}

$('#cmd input').on('click change', ev => {
    // Start a new user search

    ev.preventDefault()
    ev.stopPropagation()
    
    current_search = ev.target.value
    current_page = 0
    search()
})

$('#cmd .folder').on('click', ev => {
    // Open ressource folder
    $.get('/open')
})

$('#cmd .reload').on('click', ev => {
    // Reload ressource
    $.get('/refresh', response => {
        if (response === 'ok') {
            return location.reload()
        }

        alert('Error while loading: ' + response)
    })
})

$(window).scroll(() => {
    // Add more content as user scroll

    if ($(window).scrollTop() ==
        $(document).height() - $(window).height()) {

        current_page += 1
        search()
    }
})

// First page load
search()

// EOF