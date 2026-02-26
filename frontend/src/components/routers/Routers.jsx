import React from 'react'
import {  Routes, Route } from 'react-router-dom'
import Home from '../pages/Home'
import Contact from '../pages/Contact'
import Work from '../pages/Work'


function Routers() {
  return (
    <Routes>
        
            <Route path='/' element={<Home/>}/>
            <Route path='/contact' element={<Contact/>}/>
            <Route path='/work' element={<Work/>}/>
        
    </Routes>
  )
}

export default Routers