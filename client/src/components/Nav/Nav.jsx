import React from 'react'
import './nav.css'
import { NavLink } from 'react-router-dom'
import { Navbar, Nav } from 'react-bootstrap'
import logo from '../../assets/react-logo.png'

const Navigation = () => {
  return (
    <section id='nav'>
        <div className="container nav__container">
            <Navbar bg="primary" variant="dark" fixed="top">
            <Navbar.Brand href="/Header">
            <img src={logo} alt="brand-logo" className="img-logo"/>{' '}
             Menu </Navbar.Brand>
            <Nav className="mr-auto">
                <Nav.Link as={NavLink} to="/Bci" activeClassName="active">BCI</Nav.Link>
            </Nav>
            <Nav className="mr-auto">
                <Nav.Link as={NavLink} to="/Pec" activeClassName="active">PEC</Nav.Link>
            </Nav>
            <Nav className="mr-auto">
                <Nav.Link as={NavLink} to="/Cceup" activeClassName="active">CCEUP</Nav.Link>
            </Nav>

        </Navbar>
        </div>
    </section>
  )
}

export default Navigation
