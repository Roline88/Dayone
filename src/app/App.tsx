import { useState } from "react";
import {
  Home,
  Users,
  TestTube2,
  AlertTriangle,
  Search,
  Plus,
  Phone,
  FileText,
  Camera,
  Check,
  ChevronLeft,
  MapPin,
  Navigation,
  Play,
  X,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

// Types
type StatusType = "stable" | "monitor" | "urgent";
type TestType = "blood-pressure" | "iron" | "glucose" | "urine-protein";

interface Patient {
  id: string;
  name: string;
  age: number;
  gestationalWeeks: number;
  village: string;
  status: StatusType;
  nextTest: string;
  lastVisit: string;
  phone: string;
  emergencyContact: string;
  dueDate: string;
  pregnancyStart: string;
  notes: string;
}

interface TestResult {
  date: string;
  value: string;
  numericValue?: number;
  status: StatusType;
  notes?: string;
  done: boolean;
}

interface Test {
  type: TestType;
  name: string;
  device: string;
  purpose: string;
  latestResult: string;
  status: StatusType;
  history: TestResult[];
  videoUrl?: string;
}

interface HealthCenter {
  id: string;
  name: string;
  type: "hospital" | "clinic" | "health-center";
  distance: string;
  lat: number;
  lng: number;
  phone: string;
  capabilities: string[];
}

// Sample data
const samplePatients: Patient[] = [
  {
    id: "1",
    name: "Amina Diallo",
    age: 24,
    gestationalWeeks: 22,
    village: "Kolda Village",
    status: "monitor",
    nextTest: "Blood pressure today",
    lastVisit: "2 days ago",
    phone: "+221 77 123 4567",
    emergencyContact: "Ibrahim Diallo +221 77 234 5678",
    dueDate: "October 15, 2026",
    pregnancyStart: "February 10, 2026",
    notes: "History of mild anemia",
  },
  {
    id: "2",
    name: "Fatou Sarr",
    age: 31,
    gestationalWeeks: 16,
    village: "Thiès District",
    status: "stable",
    nextTest: "Iron test tomorrow",
    lastVisit: "1 week ago",
    phone: "+221 77 345 6789",
    emergencyContact: "Moussa Sarr +221 77 456 7890",
    dueDate: "December 20, 2026",
    pregnancyStart: "April 5, 2026",
    notes: "Second pregnancy, no complications",
  },
  {
    id: "3",
    name: "Mariama Ndiaye",
    age: 19,
    gestationalWeeks: 34,
    village: "Ziguinchor",
    status: "urgent",
    nextTest: "Urine protein today",
    lastVisit: "Today",
    phone: "+221 77 567 8901",
    emergencyContact: "Awa Ndiaye +221 77 678 9012",
    dueDate: "July 28, 2026",
    pregnancyStart: "October 20, 2025",
    notes: "High BP reading at last visit, needs monitoring",
  },
];

const healthCenters: HealthCenter[] = [
  {
    id: "1",
    name: "Regional Hospital Ziguinchor",
    type: "hospital",
    distance: "47 km",
    lat: 12.5833,
    lng: -16.2667,
    phone: "+221 33 991 1234",
    capabilities: ["Emergency care", "Maternity ward", "Surgery", "ICU"],
  },
  {
    id: "2",
    name: "Kolda Health Center",
    type: "health-center",
    distance: "23 km",
    lat: 12.9,
    lng: -14.95,
    phone: "+221 33 996 5678",
    capabilities: ["Prenatal care", "Basic emergency", "Laboratory"],
  },
  {
    id: "3",
    name: "Sédhiou District Hospital",
    type: "hospital",
    distance: "65 km",
    lat: 12.7083,
    lng: -15.5569,
    phone: "+221 33 995 2345",
    capabilities: ["Emergency care", "Maternity ward", "Surgery"],
  },
  {
    id: "4",
    name: "Vélingara Clinic",
    type: "clinic",
    distance: "38 km",
    lat: 13.15,
    lng: -14.1167,
    phone: "+221 33 998 7890",
    capabilities: ["Prenatal care", "Basic emergency"],
  },
];

const sampleTests: Record<string, Test> = {
  "blood-pressure": {
    type: "blood-pressure",
    name: "Blood Pressure",
    device: "Cradle BP Monitor",
    purpose: "Hypertension / preeclampsia risk",
    latestResult: "145/92 mmHg",
    status: "monitor",
    videoUrl: "https://example.com/bp-tutorial",
    history: [
      { date: "Jun 4", value: "145/92 mmHg", numericValue: 145, status: "monitor", done: false },
      { date: "Jun 2", value: "145/92 mmHg", numericValue: 145, status: "monitor", done: true },
      { date: "May 29", value: "138/88 mmHg", numericValue: 138, status: "monitor", done: true },
      { date: "May 25", value: "120/78 mmHg", numericValue: 120, status: "stable", done: true },
      { date: "May 20", value: "118/76 mmHg", numericValue: 118, status: "stable", done: true },
      { date: "May 15", value: "122/80 mmHg", numericValue: 122, status: "stable", done: true },
      { date: "May 10", value: "125/82 mmHg", numericValue: 125, status: "stable", done: true },
      { date: "May 5", value: "119/77 mmHg", numericValue: 119, status: "stable", done: true },
      { date: "Apr 28", value: "121/79 mmHg", numericValue: 121, status: "stable", done: true },
      { date: "Apr 20", value: "117/75 mmHg", numericValue: 117, status: "stable", done: true },
    ],
  },
  iron: {
    type: "iron",
    name: "Iron / Anemia",
    device: "Hemoglobin test",
    purpose: "Anemia screening",
    latestResult: "10.2 g/dL",
    status: "monitor",
    videoUrl: "https://example.com/iron-tutorial",
    history: [
      { date: "Jun 2", value: "10.2 g/dL", numericValue: 10.2, status: "monitor", done: true },
      { date: "May 20", value: "11.0 g/dL", numericValue: 11.0, status: "stable", done: true },
      { date: "May 5", value: "11.5 g/dL", numericValue: 11.5, status: "stable", done: true },
      { date: "Apr 20", value: "11.8 g/dL", numericValue: 11.8, status: "stable", done: true },
      { date: "Apr 5", value: "12.0 g/dL", numericValue: 12.0, status: "stable", done: true },
      { date: "Mar 20", value: "12.2 g/dL", numericValue: 12.2, status: "stable", done: true },
    ],
  },
  glucose: {
    type: "glucose",
    name: "Glucose",
    device: "Blood glucose meter",
    purpose: "Gestational diabetes screening",
    latestResult: "92 mg/dL",
    status: "stable",
    videoUrl: "https://example.com/glucose-tutorial",
    history: [
      { date: "Jun 2", value: "92 mg/dL", numericValue: 92, status: "stable", done: true },
      { date: "May 20", value: "88 mg/dL", numericValue: 88, status: "stable", done: true },
      { date: "May 5", value: "85 mg/dL", numericValue: 85, status: "stable", done: true },
      { date: "Apr 20", value: "90 mg/dL", numericValue: 90, status: "stable", done: true },
      { date: "Apr 5", value: "87 mg/dL", numericValue: 87, status: "stable", done: true },
      { date: "Mar 20", value: "89 mg/dL", numericValue: 89, status: "stable", done: true },
    ],
  },
  "urine-protein": {
    type: "urine-protein",
    name: "Urine Protein",
    device: "Urine dipstick",
    purpose: "Preeclampsia and kidney warning signs",
    latestResult: "Trace",
    status: "monitor",
    videoUrl: "https://example.com/urine-tutorial",
    history: [
      { date: "Jun 4", value: "Trace", status: "monitor", done: false },
      { date: "Jun 2", value: "Trace", status: "monitor", done: true },
      { date: "May 29", value: "Negative", status: "stable", done: true },
      { date: "May 20", value: "Negative", status: "stable", done: true },
      { date: "May 5", value: "Negative", status: "stable", done: true },
      { date: "Apr 20", value: "Negative", status: "stable", done: true },
    ],
  },
};

export default function App() {
  const [currentView, setCurrentView] = useState<"home" | "patients" | "tests" | "alerts">("home");
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null);
  const [selectedTest, setSelectedTest] = useState<Test | null>(null);
  const [showReferral, setShowReferral] = useState(false);
  const [showRecordResult, setShowRecordResult] = useState(false);
  const [selectedTestToRecord, setSelectedTestToRecord] = useState<TestResult | null>(null);

  const getStatusColor = (status: StatusType) => {
    switch (status) {
      case "stable":
        return "bg-[#10B981] text-white";
      case "monitor":
        return "bg-[#F97316] text-white";
      case "urgent":
        return "bg-[#EF4444] text-white";
    }
  };

  const getStatusText = (status: StatusType) => {
    switch (status) {
      case "stable":
        return "Stable";
      case "monitor":
        return "Monitor closely";
      case "urgent":
        return "Needs intervention";
    }
  };

  // Bottom Navigation Component
  const BottomNav = () => (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-border">
      <div className="flex justify-around items-center h-20 max-w-4xl mx-auto px-4">
        <button
          onClick={() => {
            setCurrentView("home");
            setSelectedPatient(null);
            setSelectedTest(null);
            setShowReferral(false);
            setShowRecordResult(false);
          }}
          className={`flex flex-col items-center gap-1 px-4 py-2 rounded-lg transition-colors ${
            currentView === "home" ? "text-primary" : "text-muted-foreground"
          }`}
        >
          <Home className="w-6 h-6" />
          <span className="text-sm font-medium">Home</span>
        </button>
        <button
          onClick={() => {
            setCurrentView("patients");
            setSelectedPatient(null);
            setSelectedTest(null);
            setShowReferral(false);
            setShowRecordResult(false);
          }}
          className={`flex flex-col items-center gap-1 px-4 py-2 rounded-lg transition-colors ${
            currentView === "patients" ? "text-primary" : "text-muted-foreground"
          }`}
        >
          <Users className="w-6 h-6" />
          <span className="text-sm font-medium">Patients</span>
        </button>
        <button
          onClick={() => {
            setCurrentView("tests");
            setSelectedPatient(null);
            setSelectedTest(null);
            setShowReferral(false);
            setShowRecordResult(false);
          }}
          className={`flex flex-col items-center gap-1 px-4 py-2 rounded-lg transition-colors ${
            currentView === "tests" ? "text-primary" : "text-muted-foreground"
          }`}
        >
          <TestTube2 className="w-6 h-6" />
          <span className="text-sm font-medium">Tests</span>
        </button>
        <button
          onClick={() => {
            setCurrentView("alerts");
            setSelectedPatient(null);
            setSelectedTest(null);
            setShowReferral(false);
            setShowRecordResult(false);
          }}
          className={`flex flex-col items-center gap-1 px-4 py-2 rounded-lg transition-colors ${
            currentView === "alerts" ? "text-primary" : "text-muted-foreground"
          }`}
        >
          <AlertTriangle className="w-6 h-6" />
          <span className="text-sm font-medium">Alerts</span>
        </button>
      </div>
    </div>
  );

  // Top Bar Component
  const TopBar = ({ title, showBack = false }: { title: string; showBack?: boolean }) => (
    <div className="bg-white border-b border-border">
      <div className="flex items-center justify-between h-16 px-6 max-w-4xl mx-auto">
        <div className="flex items-center gap-4">
          {showBack && (
            <button
              onClick={() => {
                if (showRecordResult) {
                  setShowRecordResult(false);
                } else if (showReferral) {
                  setShowReferral(false);
                } else if (selectedTest) {
                  setSelectedTest(null);
                } else if (selectedPatient) {
                  setSelectedPatient(null);
                }
              }}
              className="p-2 hover:bg-muted rounded-lg transition-colors"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>
          )}
          <h1 className="text-xl font-medium">{title}</h1>
        </div>
      </div>
    </div>
  );

  // Home / Patient List View
  const HomeView = () => (
    <div className="pb-24">
      <TopBar title="Good morning" />
      <div className="max-w-4xl mx-auto px-6 py-6">
        <div className="flex items-center gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search patient"
              className="w-full h-12 pl-11 pr-4 rounded-lg bg-white border border-border focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>
          <button className="flex items-center gap-2 h-12 px-6 bg-primary text-primary-foreground rounded-lg font-medium hover:opacity-90 transition-opacity">
            <Plus className="w-5 h-5" />
            Add new patient
          </button>
        </div>

        <div className="space-y-4">
          {samplePatients.map((patient) => (
            <button
              key={patient.id}
              onClick={() => setSelectedPatient(patient)}
              className="w-full bg-white rounded-lg border border-border p-6 hover:shadow-md transition-shadow text-left"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="text-lg font-medium mb-1">{patient.name}</h3>
                  <p className="text-sm text-muted-foreground">
                    {patient.age} years old · {patient.gestationalWeeks} weeks pregnant
                  </p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(patient.status)}`}>
                  {getStatusText(patient.status)}
                </span>
              </div>
              <div className="space-y-2 text-sm">
                <p className="text-muted-foreground">{patient.village}</p>
                <p className="font-medium">Next test: {patient.nextTest}</p>
                <p className="text-muted-foreground">Last visit: {patient.lastVisit}</p>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );

  // Referral Map View
  const ReferralView = () => (
    <div className="pb-24">
      <TopBar title="Nearby Health Centers" showBack />
      <div className="max-w-4xl mx-auto">
        {/* Map placeholder */}
        <div className="relative h-96 bg-muted">
          <div className="absolute inset-0 bg-[#E5E3DF]">
            {/* Simple map illustration with markers */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="relative w-full h-full">
                {/* Current location */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
                  <div className="w-4 h-4 bg-primary rounded-full border-4 border-white shadow-lg" />
                  <div className="absolute top-6 left-1/2 -translate-x-1/2 whitespace-nowrap text-xs font-medium bg-white px-2 py-1 rounded shadow">
                    Your location
                  </div>
                </div>
                {/* Hospital markers - far away */}
                <div className="absolute top-[20%] left-[70%]">
                  <MapPin className="w-8 h-8 text-[#EF4444]" />
                </div>
                <div className="absolute top-[65%] left-[25%]">
                  <MapPin className="w-7 h-7 text-[#F97316]" />
                </div>
                <div className="absolute top-[30%] right-[10%]">
                  <MapPin className="w-8 h-8 text-[#EF4444]" />
                </div>
                <div className="absolute bottom-[25%] left-[15%]">
                  <MapPin className="w-6 h-6 text-[#60A5FA]" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Health centers list */}
        <div className="px-6 py-6 space-y-4">
          {healthCenters.map((center) => (
            <div key={center.id} className="bg-white rounded-lg border border-border p-6">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <MapPin className={`w-5 h-5 ${
                      center.type === "hospital" ? "text-[#EF4444]" :
                      center.type === "health-center" ? "text-[#F97316]" :
                      "text-[#60A5FA]"
                    }`} />
                    <h3 className="text-lg font-medium">{center.name}</h3>
                  </div>
                  <p className="text-sm text-muted-foreground capitalize mb-2">{center.type.replace("-", " ")}</p>
                  <div className="flex items-center gap-4 text-sm mb-3">
                    <span className="flex items-center gap-1">
                      <Navigation className="w-4 h-4" />
                      <span className="font-medium">{center.distance}</span>
                    </span>
                    <span className="text-muted-foreground">{center.phone}</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {center.capabilities.map((cap, i) => (
                      <span key={i} className="text-xs px-2 py-1 bg-muted rounded">
                        {cap}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
              <div className="flex gap-3 mt-4">
                <button className="flex-1 h-10 bg-primary text-primary-foreground rounded-lg font-medium hover:opacity-90 transition-opacity flex items-center justify-center gap-2">
                  <Phone className="w-4 h-4" />
                  Call
                </button>
                <button className="flex-1 h-10 bg-white border border-border rounded-lg font-medium hover:bg-muted transition-colors flex items-center justify-center gap-2">
                  <Navigation className="w-4 h-4" />
                  Directions
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // Patient Profile View
  const PatientProfileView = ({ patient }: { patient: Patient }) => {
    const tests = Object.values(sampleTests);

    return (
      <div className="pb-24">
        <TopBar title={patient.name} showBack />
        <div className="max-w-4xl mx-auto px-6 py-6">
          {/* Patient Info Card */}
          <div className="bg-white rounded-lg border border-border p-6 mb-6">
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Age</p>
                <p className="font-medium">{patient.age} years</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-1">Gestational age</p>
                <p className="font-medium">{patient.gestationalWeeks} weeks</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-1">Village</p>
                <p className="font-medium">{patient.village}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-1">Due date</p>
                <p className="font-medium">{patient.dueDate}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-1">Phone</p>
                <p className="font-medium">{patient.phone}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-1">Last visit</p>
                <p className="font-medium">{patient.lastVisit}</p>
              </div>
            </div>
            <div className="pt-4 border-t border-border">
              <p className="text-sm text-muted-foreground mb-1">Emergency contact</p>
              <p className="font-medium">{patient.emergencyContact}</p>
            </div>
          </div>

          {/* Today's Action Card */}
          <div className="bg-[#60A5FA]/10 rounded-lg border border-[#60A5FA]/20 p-4 mb-6">
            <p className="font-medium text-[#1A1A1A]">
              Blood pressure and urine protein should be checked today.
            </p>
          </div>

          {/* Test Cards */}
          <div className="mb-6">
            <h2 className="text-lg font-medium mb-4">Health Status</h2>
            <div className="grid grid-cols-2 gap-4">
              {tests.map((test) => (
                <button
                  key={test.type}
                  onClick={() => setSelectedTest(test)}
                  className="bg-white rounded-lg border border-border p-4 hover:shadow-md transition-shadow text-left"
                >
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="font-medium">{test.name}</h3>
                    <div className={`w-3 h-3 rounded-full ${getStatusColor(test.status).split(" ")[0]}`} />
                  </div>
                  <div className="mb-3">
                    <p className="text-2xl font-mono font-medium mb-1">{test.latestResult}</p>
                    <p className="text-xs text-muted-foreground">{test.device}</p>
                  </div>
                  {/* Mini trend line */}
                  <div className="flex items-end gap-1 h-8 mb-3">
                    {test.history.slice(0, 4).reverse().map((result, i) => {
                      const height = test.status === "stable" ? 60 : test.status === "monitor" ? 80 : 95;
                      return (
                        <div
                          key={i}
                          className={`flex-1 rounded-sm ${
                            result.status === "stable"
                              ? "bg-[#10B981]/30"
                              : result.status === "monitor"
                                ? "bg-[#F97316]/30"
                                : "bg-[#EF4444]/30"
                          }`}
                          style={{ height: `${height - i * 5}%` }}
                        />
                      );
                    })}
                  </div>
                  <div className="text-sm font-medium text-primary">Open test →</div>
                </button>
              ))}
            </div>
          </div>

          {/* Recommendation Card */}
          <div
            className={`rounded-lg border p-4 mb-6 ${
              patient.status === "stable"
                ? "bg-[#10B981]/10 border-[#10B981]/20"
                : patient.status === "monitor"
                  ? "bg-[#F97316]/10 border-[#F97316]/20"
                  : "bg-[#EF4444]/10 border-[#EF4444]/20"
            }`}
          >
            <p className="font-medium">
              {patient.status === "stable"
                ? "All good — continue routine monitoring."
                : patient.status === "monitor"
                  ? "Needs monitoring — repeat test and follow up."
                  : "Needs intervention — refer to clinic or supervisor."}
            </p>
          </div>

          {/* Action Buttons */}
          <div className="grid grid-cols-3 gap-4">
            <button className="h-12 bg-white border border-border rounded-lg font-medium hover:bg-muted transition-colors flex items-center justify-center gap-2">
              <Phone className="w-5 h-5" />
              Call supervisor
            </button>
            <button
              onClick={() => setShowReferral(true)}
              className="h-12 bg-white border border-border rounded-lg font-medium hover:bg-muted transition-colors flex items-center justify-center gap-2"
            >
              <FileText className="w-5 h-5" />
              Create referral
            </button>
            <button className="h-12 bg-primary text-primary-foreground rounded-lg font-medium hover:opacity-90 transition-opacity flex items-center justify-center gap-2">
              <Plus className="w-5 h-5" />
              Add notes
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Test Detail View with Video Tutorial and History
  const TestView = ({ test }: { test: Test }) => {
    const todayTests = test.history.filter(t => !t.done);
    const completedTests = test.history.filter(t => t.done);
    const chartData = completedTests.slice(0, 10).reverse().map(t => ({
      date: t.date,
      value: t.numericValue || 0,
    }));

    return (
      <div className="pb-24">
        <TopBar title={test.name} showBack />
        <div className="max-w-4xl mx-auto px-6 py-6">
          {/* Test Info Card */}
          <div className="bg-white rounded-lg border border-border p-6 mb-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Device</p>
                <p className="font-medium">{test.device}</p>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(test.status)}`}>
                {getStatusText(test.status)}
              </span>
            </div>
            <div className="mb-4">
              <p className="text-sm text-muted-foreground mb-1">Latest result</p>
              <p className="text-3xl font-mono font-medium">{test.latestResult}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground mb-1">Purpose</p>
              <p className="text-sm">{test.purpose}</p>
            </div>
          </div>

          {/* Video Tutorial */}
          <div className="bg-white rounded-lg border border-border p-6 mb-6">
            <h3 className="font-medium mb-4">How to perform this test</h3>
            <div className="relative aspect-video bg-muted rounded-lg flex items-center justify-center">
              <button className="flex flex-col items-center gap-2 hover:opacity-80 transition-opacity">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center">
                  <Play className="w-8 h-8 text-white ml-1" />
                </div>
                <span className="text-sm font-medium">Watch video tutorial</span>
              </button>
            </div>
          </div>

          {/* Tests to do today */}
          {todayTests.length > 0 && (
            <div className="bg-white rounded-lg border border-border p-6 mb-6">
              <h3 className="font-medium mb-4">Tests scheduled for today</h3>
              <div className="space-y-3">
                {todayTests.map((testItem, i) => (
                  <button
                    key={i}
                    onClick={() => {
                      setSelectedTestToRecord(testItem);
                      setShowRecordResult(true);
                    }}
                    className="w-full flex items-center justify-between p-4 bg-[#60A5FA]/10 border border-[#60A5FA]/20 rounded-lg hover:bg-[#60A5FA]/20 transition-colors"
                  >
                    <div className="text-left">
                      <p className="font-medium">{test.name}</p>
                      <p className="text-sm text-muted-foreground">Due today - {testItem.date}</p>
                    </div>
                    <div className="text-primary font-medium">Record result →</div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* History Chart */}
          {chartData.length > 0 && (
            <div className="bg-white rounded-lg border border-border p-6 mb-6">
              <h3 className="font-medium mb-4">Results over time</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E7E5E4" />
                    <XAxis
                      dataKey="date"
                      stroke="#78716C"
                      style={{ fontSize: '12px', fontFamily: 'var(--font-sans)' }}
                    />
                    <YAxis
                      stroke="#78716C"
                      style={{ fontSize: '12px', fontFamily: 'var(--font-mono)' }}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#FFFFFF',
                        border: '1px solid #E7E5E4',
                        borderRadius: '8px',
                        fontFamily: 'var(--font-sans)'
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="value"
                      stroke="#60A5FA"
                      strokeWidth={2}
                      dot={{ fill: '#60A5FA', r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* Test History Table */}
          <div className="bg-white rounded-lg border border-border p-6">
            <h3 className="font-medium mb-4">Test history</h3>
            <div className="space-y-3">
              {test.history.map((result, i) => (
                <div key={i} className="flex items-center justify-between py-3 border-b border-border last:border-0">
                  <div className="flex items-center gap-4">
                    <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                      result.done
                        ? 'bg-[#10B981] border-[#10B981]'
                        : 'border-border bg-white'
                    }`}>
                      {result.done && <Check className="w-3 h-3 text-white" />}
                    </div>
                    <div>
                      <p className="font-mono font-medium">{result.value}</p>
                      <p className="text-sm text-muted-foreground">{result.date}</p>
                    </div>
                  </div>
                  <span
                    className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(result.status)}`}
                  >
                    {result.done ? getStatusText(result.status) : 'Pending'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Record Result View
  const RecordResultView = () => {
    if (!selectedTest) return null;

    return (
      <div className="pb-24">
        <TopBar title={`Record ${selectedTest.name}`} showBack />
        <div className="max-w-4xl mx-auto px-6 py-6">
          {/* Result Input */}
          <div className="bg-white rounded-lg border border-border p-6 mb-6">
            <h3 className="font-medium mb-4">Capture result</h3>
            <button className="w-full h-32 border-2 border-dashed border-border rounded-lg flex flex-col items-center justify-center gap-2 hover:border-primary hover:bg-primary/5 transition-colors mb-4">
              <Camera className="w-8 h-8 text-muted-foreground" />
              <span className="font-medium">Take photo of result</span>
            </button>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium mb-2">Manual entry (backup)</label>
                <input
                  type="text"
                  placeholder="Enter result value"
                  className="w-full h-12 px-4 rounded-lg bg-input-background border border-border focus:outline-none focus:ring-2 focus:ring-ring font-mono"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Notes</label>
                <textarea
                  placeholder="Any symptoms or observations..."
                  className="w-full h-24 px-4 py-3 rounded-lg bg-input-background border border-border focus:outline-none focus:ring-2 focus:ring-ring resize-none"
                />
              </div>
            </div>
          </div>

          {/* Interpretation */}
          <div
            className={`rounded-lg border p-4 mb-6 ${
              selectedTest.status === "stable"
                ? "bg-[#10B981]/10 border-[#10B981]/20"
                : selectedTest.status === "monitor"
                  ? "bg-[#F97316]/10 border-[#F97316]/20"
                  : "bg-[#EF4444]/10 border-[#EF4444]/20"
            }`}
          >
            <p className="font-medium mb-2">
              {selectedTest.status === "stable"
                ? "Result looks normal."
                : selectedTest.status === "monitor"
                  ? "Repeat or monitor closely."
                  : "Possible risk — contact supervisor or refer."}
            </p>
            <p className="text-sm">
              {selectedTest.status === "stable"
                ? "Continue routine follow-up"
                : selectedTest.status === "monitor"
                  ? "Repeat test in 30 minutes or schedule another visit"
                  : "Refer patient to clinic immediately"}
            </p>
          </div>

          {/* Save Button */}
          <button className="w-full h-12 bg-primary text-primary-foreground rounded-lg font-medium hover:opacity-90 transition-opacity flex items-center justify-center gap-2">
            <Check className="w-5 h-5" />
            Save result
          </button>
        </div>
      </div>
    );
  };

  // Alerts View
  const AlertsView = () => {
    const urgentPatients = samplePatients.filter((p) => p.status === "urgent" || p.status === "monitor");

    return (
      <div className="pb-24">
        <TopBar title="Alerts" />
        <div className="max-w-4xl mx-auto px-6 py-6">
          <div className="space-y-4">
            {urgentPatients.map((patient) => (
              <div
                key={patient.id}
                className={`rounded-lg border p-6 ${
                  patient.status === "urgent"
                    ? "bg-[#EF4444]/10 border-[#EF4444]/20"
                    : "bg-[#F97316]/10 border-[#F97316]/20"
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="text-lg font-medium mb-1">{patient.name}</h3>
                    <p className="text-sm text-muted-foreground">
                      {patient.age} years · {patient.gestationalWeeks} weeks
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(patient.status)}`}>
                    {getStatusText(patient.status)}
                  </span>
                </div>
                <p className="font-medium mb-4">
                  {patient.status === "urgent"
                    ? "High blood pressure + protein in urine detected. Refer to clinic."
                    : "Low iron and elevated blood pressure. Monitor and follow up."}
                </p>
                <button
                  onClick={() => setSelectedPatient(patient)}
                  className="h-12 w-full bg-white border border-border rounded-lg font-medium hover:bg-muted transition-colors"
                >
                  Open patient profile
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Tests List View
  const TestsListView = () => {
    const tests = Object.values(sampleTests);

    return (
      <div className="pb-24">
        <TopBar title="All Tests" />
        <div className="max-w-4xl mx-auto px-6 py-6">
          <div className="space-y-4">
            {tests.map((test) => (
              <button
                key={test.type}
                onClick={() => setSelectedTest(test)}
                className="w-full bg-white rounded-lg border border-border p-6 hover:shadow-md transition-shadow text-left"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="text-lg font-medium mb-1">{test.name}</h3>
                    <p className="text-sm text-muted-foreground">{test.device}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(test.status)}`}>
                    {getStatusText(test.status)}
                  </span>
                </div>
                <p className="text-sm text-muted-foreground mb-3">{test.purpose}</p>
                <p className="text-2xl font-mono font-medium">{test.latestResult}</p>
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Main render
  if (showRecordResult && selectedTest) {
    return (
      <>
        <RecordResultView />
        <BottomNav />
      </>
    );
  }

  if (showReferral) {
    return (
      <>
        <ReferralView />
        <BottomNav />
      </>
    );
  }

  if (selectedTest) {
    return (
      <>
        <TestView test={selectedTest} />
        <BottomNav />
      </>
    );
  }

  if (selectedPatient) {
    return (
      <>
        <PatientProfileView patient={selectedPatient} />
        <BottomNav />
      </>
    );
  }

  return (
    <>
      {currentView === "home" && <HomeView />}
      {currentView === "patients" && <HomeView />}
      {currentView === "tests" && <TestsListView />}
      {currentView === "alerts" && <AlertsView />}
      <BottomNav />
    </>
  );
}
