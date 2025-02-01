import re
import random
import typing
from PyWebRequests.data import (
	UserAgentBrowser,
	UserAgentEngine,
	UserAgentOS,
	UserAgentSupportedParts
)
from PyWebRequests.data_types import (
	supported_ua_browsers,
	supported_ua_engines,
	supported_ua_platforms
)


def generate_yandex_ua() -> str:
	yandex_browser_version = random.choice(UserAgentBrowser.yandex_versions)
	
	return f"YaBrowser/{yandex_browser_version}"


def generate_edge_ua() -> str:
	edge_version = random.choice(UserAgentBrowser.edge_versions)
	
	return f"Edg/{edge_version}"


def generate_opera_ua() -> str:
	opera_version = random.choice(UserAgentBrowser.opera_versions)
	
	return f"Opera/{opera_version}"


def generate_firefox_ua() -> str:
	firefox_version = random.choice(UserAgentBrowser.firefox_versions)
	
	return f"Firefox/{firefox_version}"


def generate_safari_ua(engine_ua: typing.Optional[str] = None) -> str:
	if engine_ua is None or re.search(r"AppleWebKit/(\d+(?:\.\d+)*)", engine_ua) is None:
		version_parts = [str(random.choice(UserAgentEngine.apple_webkit_versions[0]))]
	
		if random.choice([True, False]):
			version_parts.append(str(random.choice(UserAgentEngine.apple_webkit_versions[1])))
	
			if random.choice([True, False]):
				version_parts.append(str(random.choice(UserAgentEngine.apple_webkit_versions[2])))
	
		safari_version = ".".join(version_parts)
	else:
		webkit_version: list[str] = re.search(r"AppleWebKit/(\d+(?:\.\d+)*)", engine_ua).group(1).split(".")
		webkit_version[0] = str(
				int(webkit_version[0]) + random.randint(
						0,
						min(20, max(UserAgentEngine.apple_webkit_versions[0]) - int(webkit_version[0]))
				)
		)
	
		safari_version = ".".join(webkit_version)
	
	return f"Safari/{safari_version}"


def generate_chrome_ua() -> str:
	chrome_version = random.choice(UserAgentBrowser.chrome_versions)
	
	return f"Chrome/{chrome_version}"


def generate_random_browser_ua(
		browser_to_generate: typing.Optional[supported_ua_browsers] = None,
		engine: typing.Optional[supported_ua_engines] = None,
		engine_ua: typing.Optional[str] = None
) -> tuple[str, str]:
	if engine is not None and engine not in UserAgentSupportedParts.engine:
		raise ValueError(f"Unsupported engine ({engine})")
	
	if browser_to_generate is None:
		if engine is None:
			browser_to_generate = random.choice(UserAgentSupportedParts.browser)
		elif engine == "AppleWebKit":
			browser_to_generate = random.choice(UserAgentSupportedParts.apple_webkit_browsers)
		elif engine == "Blink":
			browser_to_generate = random.choice(UserAgentSupportedParts.blink_browsers)
		elif engine == "Gecko":
			browser_to_generate = random.choice(UserAgentSupportedParts.gecko_browsers)
	
	if browser_to_generate == "Chrome":
		chrome_ua = generate_chrome_ua()
		safari_ua = generate_safari_ua(engine_ua)
	
		return f"{chrome_ua} {safari_ua}", browser_to_generate
	elif browser_to_generate == "Firefox":
		return generate_firefox_ua(), browser_to_generate
	elif browser_to_generate == "Safari":
		return generate_safari_ua(engine_ua), browser_to_generate
	elif browser_to_generate == "Opera":
		chrome_ua = generate_chrome_ua()
		opera_ua = generate_opera_ua()
		safari_ua = generate_safari_ua(engine_ua)
	
		return f"{chrome_ua} {opera_ua} {safari_ua}", browser_to_generate
	elif browser_to_generate == "Edge":
		chrome_ua = generate_chrome_ua()
		yandex_ua = generate_edge_ua()
		safari_ua = generate_safari_ua(engine_ua)
	
		return f"{chrome_ua} {yandex_ua} {safari_ua}", browser_to_generate
	elif browser_to_generate == "Yandex":
		chrome_ua = generate_chrome_ua()
		yandex_ua = generate_yandex_ua()
		safari_ua = generate_safari_ua(engine_ua)
	
		return f"{chrome_ua} {yandex_ua} {safari_ua}", browser_to_generate
	else:
		raise ValueError(f"Unsupported browser ({browser_to_generate})")


def generate_random_gecko_ua() -> str:
	year = random.choice(UserAgentEngine.gecko_versions[0])
	month = random.choice(UserAgentEngine.gecko_versions[1])
	
	if month in [1, 3, 5, 7, 8, 10, 12]:
		day = random.choice(UserAgentEngine.gecko_versions[2][0])
	elif month in [4, 6, 9, 11]:
		day = random.choice(UserAgentEngine.gecko_versions[2][1])
	elif year % 4 == 0:
		day = random.choice(UserAgentEngine.gecko_versions[2][2])
	else:
		day = random.choice(UserAgentEngine.gecko_versions[2][3])
	
	gecko_version = f"{year}{month:02d}{day:02d}"
	return f"Gecko/{gecko_version}"


def generate_random_apple_webkit_ua() -> str:
	version_parts = [str(random.choice(UserAgentEngine.apple_webkit_versions[0]))]
	
	if random.choice([True, False]):
		version_parts.append(str(random.choice(UserAgentEngine.apple_webkit_versions[1])))
	
		if random.choice([True, False]):
			version_parts.append(str(random.choice(UserAgentEngine.apple_webkit_versions[2])))
	
	return f"AppleWebKit/{'.'.join(version_parts)} (KHTML, like Gecko)"


def generate_random_engine_ua(
		engine_to_generate: typing.Optional[supported_ua_engines] = None,
		platform: typing.Optional[supported_ua_platforms] = None
) -> tuple[str, str]:
	if platform is not None and platform not in UserAgentSupportedParts.os:
		raise ValueError(f"Unsupported OS ({platform})")
	
	if engine_to_generate is None:
		engine_to_generate = "AppleWebKit" if platform == "IOS" else random.choice(UserAgentSupportedParts.engine)
	
	if engine_to_generate == "AppleWebKit":
		return generate_random_apple_webkit_ua(), engine_to_generate
	elif engine_to_generate == "Gecko":
		return generate_random_gecko_ua(), engine_to_generate
	elif engine_to_generate == "Blink":
		return generate_random_apple_webkit_ua(), engine_to_generate
	else:
		raise ValueError(f"Unsupported engine ({engine_to_generate})")


def generate_ios_ua() -> str:
	ios_version = random.choice(UserAgentOS.ios_versions)
	device, os_prefix = random.choice(UserAgentOS.ios_devices)
	
	return f"{device}; {os_prefix} {ios_version} like Mac OS X"


def generate_android_ua() -> str:
	android_type = random.choice(["Linux", "Mobile"])
	android_version = random.choice(UserAgentOS.android_versions)
	device = random.choice(UserAgentOS.android_devices)
	
	return f"{'Linux; ' if android_type == 'Linux' else ''}Android {android_version}{'; Mobile' if android_type == 'Mobile' else ''}; {device}"


def generate_linux_ua() -> str:
	prefix = random.choice(["X11", None])
	linux_distribution = random.choice(UserAgentOS.linux_distributions)
	linux_architecture = random.choice(UserAgentOS.linux_architectures)
	
	return "; ".join(
			list(filter(None, [prefix, linux_distribution, f"Linux {linux_architecture}"]))
	)


def generate_mac_ua() -> str:
	cpu = random.choice(["Intel", "Apple Silicon"])
	macos_version = random.choice(
			UserAgentOS.mac_os_intel_versions
			if cpu == "Intel"
			else UserAgentOS.mac_os_apple_silicon_versions
	)
	
	return f"Macintosh; {cpu} Mac OS X {macos_version}"


def generate_windows_ua() -> str:
	windows_version = random.choice(UserAgentOS.windows_versions)
	windows_architecture = random.choice(UserAgentOS.windows_architectures)
	
	return f"Windows {windows_version}; {windows_architecture}"


def generate_random_os_ua(os_to_generate: typing.Optional[supported_ua_platforms] = None) -> tuple[str, str]:
	if os_to_generate is None:
		os_to_generate = random.choice(UserAgentSupportedParts.os)
	
	if os_to_generate == "Windows":
		return generate_windows_ua(), os_to_generate
	elif os_to_generate == "Macintosh":
		return generate_mac_ua(), os_to_generate
	elif os_to_generate == "Linux":
		return generate_linux_ua(), os_to_generate
	elif os_to_generate == "Android":
		return generate_android_ua(), os_to_generate
	elif os_to_generate == "IOS":
		return generate_ios_ua(), os_to_generate
	else:
		raise ValueError(f"Unsupported OS ({os_to_generate})")


def generate_random_mozilla_ua() -> str:
	return "Mozilla/5.0"


def generate_random_user_agent() -> str:
	mozilla_ua = generate_random_mozilla_ua()
	os_ua, used_os = generate_random_os_ua()
	engine_ua, used_engine = generate_random_engine_ua(platform=used_os)
	browser_ua, used_browser = generate_random_browser_ua(engine=used_engine, engine_ua=engine_ua)
	
	return f"{mozilla_ua} ({os_ua}) {engine_ua} {browser_ua}"
