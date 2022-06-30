const xhr = new XMLHttpRequest();
xhr.open(
	"GET",
	"https://api.openweathermap.org/data/2.5/weather?q=Alicante&appid=9a64d1f87c6f0905f9778babb2d8389f"
);
xhr.send();
xhr.onload = () => {
	const weather = JSON.prase(xhr.response);
	console.log(weather);
};
