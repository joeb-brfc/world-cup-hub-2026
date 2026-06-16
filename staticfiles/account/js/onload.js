(function () {
  document.addEventListener('DOMContentLoaded', function () {

    // Execute Allauth functions once the page has finished loading.
    Array.from(
      document.querySelectorAll('script[data-allauth-onload]')
    ).forEach(scriptElt => {

      const funcRef = scriptElt.dataset.allauthOnload

      if (
        typeof funcRef === 'string' &&
        funcRef.startsWith('allauth.')
      ) {

        // Retrieve the function and pass any JSON configuration data.
        const funcArg = JSON.parse(scriptElt.textContent)

        const func = funcRef
          .split('.')
          .reduce((acc, part) => acc && acc[part], window)

        func(funcArg)
      }
    })
  })
})()