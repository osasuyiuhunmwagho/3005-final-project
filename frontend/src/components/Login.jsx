import React, { useState } from 'react'
import { memberAPI, adminAPI, trainerAPI } from '../services/api'

function Login({ onLogin }) {
  const [selectedRole, setSelectedRole] = useState(null)
  const [isRegistering, setIsRegistering] = useState(false)
  const [userId, setUserId] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // Registration form state
  const [registerForm, setRegisterForm] = useState({
    name: '',
    email: '',
    date_of_birth: '',
    gender: '',
    phone: ''
  })

  const handleRoleSelect = (role) => {
    setSelectedRole(role)
    setIsRegistering(false)
    setError('')
    setSuccess('')
    // Only allow registration for members
    if (role === 'member') {
      setIsRegistering(true)
    }
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    if (!registerForm.name || !registerForm.email) {
      setError('Name and email are required')
      return
    }

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const response = await memberAPI.create(registerForm)
      if (response.data) {
        setSuccess(`Member created successfully! Your ID is ${response.data.member_id}`)
        // Auto-login after registration
        setTimeout(() => {
          onLogin('member', response.data.member_id)
        }, 1500)
      }
    } catch (err) {
      if (err.response?.status === 400) {
        setError(err.response.data.detail || 'Registration failed. Email may already exist.')
      } else {
        setError('Failed to register. Please check your backend is running.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleLogin = async () => {
    if (!selectedRole || !userId) {
      setError('Please select a role and enter an ID')
      return
    }

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      let response
      const id = parseInt(userId)

      switch (selectedRole) {
        case 'member':
          response = await memberAPI.getById(id)
          break
        case 'admin':
          response = await adminAPI.getById(id)
          break
        case 'trainer':
          response = await trainerAPI.getById(id)
          break
        default:
          throw new Error('Invalid role')
      }

      if (response.data) {
        onLogin(selectedRole, id)
      }
    } catch (err) {
      if (err.response?.status === 404) {
        setError(`${selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1)} with ID ${userId} not found. Please create one first or use an existing ID.`)
      } else {
        setError('Failed to login. Please check your backend is running.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Fitness Center Management</h2>
        <p style={{ textAlign: 'center', color: '#666', marginBottom: '30px' }}>
          Select your role and enter your ID to continue
        </p>

        <div className="role-selector">
          <div
            className={`role-button ${selectedRole === 'member' ? 'selected' : ''}`}
            onClick={() => handleRoleSelect('member')}
          >
            <h3>Member</h3>
            <p>View classes, track health</p>
          </div>
          <div
            className={`role-button ${selectedRole === 'admin' ? 'selected' : ''}`}
            onClick={() => handleRoleSelect('admin')}
          >
            <h3>Admin</h3>
            <p>Manage system</p>
          </div>
          <div
            className={`role-button ${selectedRole === 'trainer' ? 'selected' : ''}`}
            onClick={() => handleRoleSelect('trainer')}
          >
            <h3>Trainer</h3>
            <p>Set availability</p>
          </div>
        </div>

        {selectedRole === 'member' && isRegistering ? (
          <form onSubmit={handleRegister}>
            <h3 style={{ color: '#008080', marginBottom: '15px' }}>Register as Member</h3>
            <div className="form-group">
              <label>Name *</label>
              <input
                type="text"
                value={registerForm.name}
                onChange={(e) => setRegisterForm({ ...registerForm, name: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Email *</label>
              <input
                type="email"
                value={registerForm.email}
                onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })}
                required
              />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px' }}>
              <div className="form-group">
                <label>Date of Birth</label>
                <input
                  type="date"
                  value={registerForm.date_of_birth}
                  onChange={(e) => setRegisterForm({ ...registerForm, date_of_birth: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label>Gender</label>
                <select
                  value={registerForm.gender}
                  onChange={(e) => setRegisterForm({ ...registerForm, gender: e.target.value })}
                >
                  <option value="">Select...</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>
            <div className="form-group">
              <label>Phone</label>
              <input
                type="tel"
                value={registerForm.phone}
                onChange={(e) => setRegisterForm({ ...registerForm, phone: e.target.value })}
                placeholder="(optional)"
              />
            </div>
            {error && <div className="alert alert-error">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
                style={{ flex: 1 }}
              >
                {loading ? 'Registering...' : 'Register'}
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setIsRegistering(false)}
                disabled={loading}
              >
                Login Instead
              </button>
            </div>
          </form>
        ) : selectedRole && (
          <>
            <div className="form-group">
              <label>
                {selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1)} ID:
              </label>
              <input
                type="number"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder={`Enter ${selectedRole} ID`}
                onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
              />
            </div>
            {selectedRole === 'member' && (
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setIsRegistering(true)}
                style={{ width: '100%', marginBottom: '10px' }}
              >
                New Member? Register Here
              </button>
            )}
            {error && <div className="alert alert-error">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <button
              className="btn btn-primary"
              onClick={handleLogin}
              disabled={!selectedRole || !userId || loading}
              style={{ width: '100%', marginTop: '10px' }}
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </>
        )}

        {selectedRole && !isRegistering && (
          <p style={{ textAlign: 'center', marginTop: '20px', fontSize: '12px', color: '#666' }}>
            {selectedRole === 'member' 
              ? 'New members can register above. Existing members can login with their ID.'
              : 'Use Swagger docs to create users first, then login with their IDs'}
          </p>
        )}
      </div>
    </div>
  )
}

export default Login

