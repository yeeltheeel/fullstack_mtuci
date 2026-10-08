import LandingImage from '../assets/exchange.jpg'

export default function HomePage(){
    return(
        <div>
            <h1>Welcome, avid bookworm</h1>
            <img src={LandingImage} alt="Welcome"/>
        </div>
    )
}