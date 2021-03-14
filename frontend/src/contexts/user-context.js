import React from 'react'

//A user context that will store their details, accessible to all pages
export default React.createContext({
    user: null,
    setUser: () =>{}
});