import React from 'react';
import { Carousel } from 'react-bootstrap';
import wf from '../../assets/workflows.png'
import './header.css'

const Header = () => {

  return (
    <section id="header">
        <h3>WebCrawler for project database leads automation</h3>
        <div className="container header__container">
            <Carousel>
                <Carousel.Item>
                    <img className="img-carousel" src={wf} alt="First slide" />
                    <Carousel.Caption>
                        <h3>BCI Workflow</h3>
                        <p>Inputs from user: Excels from BCICentral, output is 1 csv</p>
                    </Carousel.Caption>
                </Carousel.Item>

                <Carousel.Item>
                    <img className="img-carousel" src={wf} alt="Second slide" />
                    <Carousel.Caption>
                        <h3>PEC Workflow</h3>
                        <p>Inputs from user: username, password, auth_code, start_date_str, end_date_str, output is 1 csv</p>
                    </Carousel.Caption>
                </Carousel.Item>

                <Carousel.Item>
                    <img className="img-carousel" src={wf} alt="Third slide" />
                    <Carousel.Caption>
                        <h3>CCEUP Workflow</h3>
                        <p>Input from user: 1 Excel from 中能, output is 1 csv</p>
                    </Carousel.Caption>
                </Carousel.Item>
            </Carousel>
            <br />
            <a href="mailto:Charlie.Jin@irco.com" className="text-light">Developed by Charlie Jin</a>
        </div>
    </section>
  )
}

export default Header
