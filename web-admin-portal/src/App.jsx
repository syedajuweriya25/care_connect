import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import api from './services/api'
import './App.css'

const modules = [
  { title: 'Emergency Response', description: 'Dispatch alerts and manage SOS requests in real time.' },
  { title: 'Society Management', description: 'Keep resident, gate, and visitor data organized effortlessly.' },
  { title: 'Notifications', description: 'Broadcast critical updates to residents and volunteers instantly.' },
]

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('access_token')
  return token ? children : <Navigate to="/login" replace />
}

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      setLoading(false)
      return
    }

    api.get('/api/auth/me/')
      .then(({ data }) => setUser(data))
      .catch(() => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <div className="app-shell"><div className="panel">Loading CareConnect...</div></div>
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<AuthPage onAuth={setUser} />} />
        <Route path="/register" element={<AuthPage onAuth={setUser} isRegister />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage user={user} onLogout={() => setUser(null)} />
            </ProtectedRoute>
          }
        />
        <Route path="/pending" element={<PendingPage user={user} />} />
        <Route path="/" element={<Navigate to={user ? '/dashboard' : '/login'} replace />} />
      </Routes>
    </BrowserRouter>
  )
}

function AuthPage({ isRegister = false, onAuth }) {
  const [form, setForm] = useState({
    full_name: '',
    email: '',
    phone: '',
    role: 'resident',
    password: '',
    password_confirm: '',
    role_details: {},
    blood_group: '',
    emergency_contact_name: '',
    emergency_contact_phone: '',
    medical_conditions: '',
    allergies: '',
    address: '',
  })
  const [step, setStep] = useState(1)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState('')

  const roleFields = {
    resident: { name: 'apartment_number', label: 'Apartment / Flat Number', placeholder: 'Apartment / Flat Number' },
    guardian: { name: 'dependant_name', label: 'Dependent name', placeholder: 'Dependent name' },
    volunteer: { name: 'volunteer_skills', label: 'Volunteer skills', placeholder: 'Volunteer skills' },
    security: { name: 'security_id', label: 'Security ID / Gate', placeholder: 'Security ID / Gate' },
  }

  const getRoleFieldLabel = () => roleFields[form.role]?.label || 'Role details'

  const parseResponseErrors = (data) => {
    if (!data) return 'Unable to complete request.'
    if (typeof data === 'string') return data
    if (data.detail) return data.detail

    const messages = []
    Object.entries(data).forEach(([field, value]) => {
      if (Array.isArray(value)) {
        value.forEach((item) => messages.push(`${field.replace('_', ' ')}: ${item}`))
      } else if (typeof value === 'object') {
        Object.values(value).flat().forEach((item) => messages.push(`${field.replace('_', ' ')}: ${item}`))
      } else {
        messages.push(`${field.replace('_', ' ')}: ${value}`)
      }
    })
    return messages.join(' ') || 'Unable to complete request.'
  }

  const validateStep = () => {
    const errors = []
    if (step === 1) {
      if (!form.full_name.trim()) errors.push('Full name is required.')
      if (!form.email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) errors.push('Invalid email address.')
      if (!form.phone.trim() || form.phone.replace(/\D/g, '').length !== 10) errors.push('Phone number must contain exactly 10 digits.')
      if (form.password.length < 8) errors.push('Password must contain at least 8 characters.')
      if (form.password !== form.password_confirm) errors.push('Passwords do not match.')
    }
    if (step === 2) {
      const fieldName = roleFields[form.role]?.name
      const fieldValue = form.role_details[fieldName]
      if (!fieldValue || !fieldValue.trim()) {
        errors.push(`${getRoleFieldLabel()} is required.`)
      }
    }
    if (step === 3) {
      if (!form.blood_group.trim()) errors.push('Blood group is required.')
      if (!form.emergency_contact_name.trim()) errors.push('Emergency contact name is required.')
      if (!form.emergency_contact_phone.trim() || form.emergency_contact_phone.replace(/\D/g, '').length !== 10) errors.push('Emergency contact number is invalid.')
      if (!form.address.trim()) errors.push('Address is required.')
    }

    if (errors.length > 0) {
      setError(errors.join(' '))
      return false
    }
    setError('')
    return true
  }

  const handleNext = (event) => {
    event.preventDefault()
    if (!validateStep()) return
    setStep((current) => Math.min(3, current + 1))
  }

  const handleBack = (event) => {
    event.preventDefault()
    setError('')
    setStep((current) => Math.max(1, current - 1))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (isRegister && step < 3) {
      handleNext(event)
      return
    }

    if (isRegister && !validateStep()) return

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const endpoint = isRegister ? '/api/auth/register/' : '/api/auth/login/'
      const payload = isRegister
        ? {
            full_name: form.full_name,
            email: form.email,
            phone: form.phone,
            role: form.role,
            password: form.password,
            password_confirm: form.password_confirm,
            role_details: form.role_details,
            blood_group: form.blood_group,
            emergency_contact_name: form.emergency_contact_name,
            emergency_contact_phone: form.emergency_contact_phone,
            medical_conditions: form.medical_conditions,
            allergies: form.allergies,
            address: form.address,
          }
        : { email: form.email, password: form.password }

      const { data } = await api.post(endpoint, payload)
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      onAuth(data.user)
      setSuccess('Registration successful! Redirecting to your dashboard...')
      if (data.user?.is_verified === false) {
        window.location.href = '/pending'
      } else {
        window.location.href = '/dashboard'
      }
    } catch (err) {
      setError(parseResponseErrors(err.response?.data))
    } finally {
      setLoading(false)
    }
  }

  const handleFieldChange = (field, value) => {
    setForm((current) => ({ ...current, [field]: value }))
  }

  const handleRoleDetailChange = (value) => {
    const fieldName = roleFields[form.role]?.name
    setForm((current) => ({
      ...current,
      role_details: {
        ...current.role_details,
        [fieldName]: value,
      },
    }))
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>{isRegister ? 'Create your CareConnect account' : 'Welcome back to CareConnect'}</h1>
        <p>{isRegister ? 'Complete the registration steps to join your community.' : 'Sign in to access your community tools.'}</p>
        <form className="auth-form" onSubmit={handleSubmit}>
          {isRegister ? (
            <>
              <div className="form-step">Step {step} of 3</div>
              {step === 1 && (
                <>
                  <input value={form.full_name} onChange={(event) => handleFieldChange('full_name', event.target.value)} placeholder="Full name" required />
                  <input value={form.email} onChange={(event) => handleFieldChange('email', event.target.value)} placeholder="Email" type="email" required />
                  <input value={form.phone} onChange={(event) => handleFieldChange('phone', event.target.value)} placeholder="Phone" required />
                  <select value={form.role} onChange={(event) => handleFieldChange('role', event.target.value)}>
                    <option value="resident">Resident</option>
                    <option value="guardian">Guardian</option>
                    <option value="volunteer">Volunteer</option>
                    <option value="security">Security</option>
                  </select>
                  <input type="password" value={form.password} onChange={(event) => handleFieldChange('password', event.target.value)} placeholder="Password" required />
                  <input type="password" value={form.password_confirm} onChange={(event) => handleFieldChange('password_confirm', event.target.value)} placeholder="Confirm password" required />
                </>
              )}
              {step === 2 && (
                <>
                  <label>{getRoleFieldLabel()}</label>
                  <input value={form.role_details[roleFields[form.role]?.name] || ''} onChange={(event) => handleRoleDetailChange(event.target.value)} placeholder={roleFields[form.role]?.placeholder} required />
                  <textarea value={form.medical_conditions} onChange={(event) => handleFieldChange('medical_conditions', event.target.value)} placeholder="Medical conditions (optional)" />
                  <textarea value={form.allergies} onChange={(event) => handleFieldChange('allergies', event.target.value)} placeholder="Allergies (optional)" />
                </>
              )}
              {step === 3 && (
                <>
                  <input value={form.blood_group} onChange={(event) => handleFieldChange('blood_group', event.target.value)} placeholder="Blood group" required />
                  <input value={form.emergency_contact_name} onChange={(event) => handleFieldChange('emergency_contact_name', event.target.value)} placeholder="Emergency contact name" required />
                  <input value={form.emergency_contact_phone} onChange={(event) => handleFieldChange('emergency_contact_phone', event.target.value)} placeholder="Emergency contact phone" required />
                  <input value={form.address} onChange={(event) => handleFieldChange('address', event.target.value)} placeholder="Address / Flat number" required />
                </>
              )}
              {error && <div className="error-box">{error}</div>}
              {success && <div className="success-box">{success}</div>}
              <div className="form-actions">
                {step > 1 && <button className="secondary-button" onClick={handleBack} disabled={loading}>Back</button>}
                <button type="submit" disabled={loading}>{loading ? 'Please wait...' : step < 3 ? 'Next' : 'Create account'}</button>
              </div>
            </>
          ) : (
            <>
              <input type="email" value={form.email} onChange={(event) => handleFieldChange('email', event.target.value)} placeholder="Email" required />
              <input type="password" value={form.password} onChange={(event) => handleFieldChange('password', event.target.value)} placeholder="Password" required />
              {error && <div className="error-box">{error}</div>}
              <button type="submit" disabled={loading}>{loading ? 'Please wait...' : 'Sign in'}</button>
            </>
          )}
        </form>
        <p className="auth-link">
          {isRegister ? 'Already have an account?' : "Need an account?"}{' '}
          <a href={isRegister ? '/login' : '/register'}>{isRegister ? 'Sign in' : 'Create one'}</a>
        </p>
      </div>
    </div>
  )
}

function PendingPage({ user }) {
  return (
    <div className="app-shell">
      <div className="panel">
        <h2>Verification pending</h2>
        <p>Your account is registered, but email verification is still pending.</p>
        <p className="hero-copy">You can continue using the portal while the verification process completes.</p>
        <a className="primary-action" href="/dashboard">Continue</a>
      </div>
    </div>
  )
}

function DashboardPage({ user, onLogout }) {
  return (
    <div className="app-shell">
      <header className="hero-card">
        <div>
          <p className="eyebrow">CareConnect Admin Portal</p>
          <h1>Welcome back, {user?.full_name || 'Operator'}</h1>
          <p className="hero-copy">Role: {user?.role || 'resident'}</p>
        </div>
        <button className="primary-action" onClick={() => { localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token'); onLogout(); window.location.href='/login' }}>Logout</button>
      </header>

      <main className="content-grid">
        <section className="panel">
          <h2>CareConnect operations</h2>
          <p>Your authentication flow is now connected to the Django backend and ready for protected features.</p>
        </section>
        <section className="panel">
          <h2>Core modules</h2>
          <div className="module-list">
            {modules.map((module) => (
              <article key={module.title} className="module-card">
                <h3>{module.title}</h3>
                <p>{module.description}</p>
              </article>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
