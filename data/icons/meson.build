application_id = 'com.lapas.Fbe'

scalable_dir = 'hicolor' / 'scalable' / 'apps'
scalable_icons = [
	scalable_dir / 'fbe.svg',
	scalable_dir / ('@0@.svg').format(application_id),
	scalable_dir / 'plus-symbolic.svg'
]
install_data(
  scalable_icons,
  install_dir: get_option('datadir') / 'icons' / scalable_dir
)

symbolic_dir = 'hicolor' / 'symbolic' / 'apps'
install_data(
  symbolic_dir / ('@0@-symbolic.svg').format(application_id),
  install_dir: get_option('datadir') / 'icons' / symbolic_dir
)
