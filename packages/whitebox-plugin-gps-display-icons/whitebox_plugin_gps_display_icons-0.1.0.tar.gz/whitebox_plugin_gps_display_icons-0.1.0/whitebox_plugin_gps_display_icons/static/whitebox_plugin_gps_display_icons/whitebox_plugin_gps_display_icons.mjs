const init = () => {
  const extension = Whitebox.extensions.getByName('gps_display')
  if (!extension) {
    throw new Error('Could not find gps_display extension')
  }

  const iconURL = Whitebox.apiUrl + '/static/whitebox_plugin_gps_display_icons/assets/plane.svg'
  extension.setWhiteboxMarkerIcon({
    iconURL: iconURL,
    isRotating: true,
    initialRotation: 180,
  })
}

const module = {
  name: 'gps_display_icons',
  init: init,
}

Whitebox.plugins.registerPlugin(module)

export default module
