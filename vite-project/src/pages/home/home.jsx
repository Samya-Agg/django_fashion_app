import { Fragment } from "react"; 
import './home.css'

const Homepage=()=>{
    return(
        <Fragment>  
            <div className="page1">
                <div className="topstrip">
                    <div className="logo"></div>
                     <div className="list">
                        <ul>
                            <li><a href="http://127.0.0.1:8000/store/store">Home</a></li>
                            <li><a href="http://127.0.0.1:8000/store/outfit/">Outfit Check</a></li>
                            
                            <li><a href="http://127.0.0.1:8000/store/colour/">Colour Analysis</a></li>
                            <li><a href="http://127.0.0.1:8000/store/register/">Register</a></li>
                            <li><a href="http://127.0.0.1:8000/store/login/">Login</a></li>
                            
                            
                        </ul>
                    </div> 
                </div>
                <div className="ztrendz">
                    ZTrendZ
                    <div className="genz">
                        <div>GenZ Edge</div>
                        <div className="pic"></div>
                            <div className="about">
                            <p>GenZ Edge: Fashion Forward, Future Bound. Discover the styles that are shaping tomorrow's wardrobe today</p>
                            </div>  
                    </div>              
                </div>
            </div>

              
        </Fragment>
    )        
}

export default Homepage;
