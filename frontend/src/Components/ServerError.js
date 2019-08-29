import React from 'react'

const ServerError = () => (
  <div className='container jumbotron'>
    <div className='display-4 text-warning'>OOPS!</div>
    <div className='lead'>
      Sorry, the server encountered an internal error and was enable to complete
      your request.
    </div>
    <button
      type='reset'
      className='btn btn-info'
      onClick={() => {
        window.location.href = '/'
      }}
    >
      Back to Home
    </button>
  </div>
)

export default ServerError
