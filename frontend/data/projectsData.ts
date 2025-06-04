interface Project {
  title: string
  description: string
  href?: string
  imgSrc?: string
}

const projectsData: Project[] = [
  {
    title: "Kalenuxer",
    description: "A next-generation web application framework engineered for maximum performance and flexibility. Kalenuxer delivers a comprehensive suite: multi-language support, advanced minification and obfuscation, server-side rendering, modular templating (mails, sections, pages), classification, SVG-to-icon conversion, version control, optimized CSS/JS structure, and robust localization—empowering rapid development of scalable, production-grade applications.",
    imgSrc: "static/images/kalenuxer/1.webp",
    href: "https://github.com/emirbaycan/Kalenuxer"
  },
  {
    title: "My Partners Law Firm",
    description: "Custom-built website and control panel for a leading law firm, leveraging Kalenuxer’s SSR algorithms to seamlessly convert dynamic SQL data into optimized HTML structures. Delivers real-time content updates, secure client management, and a powerful admin interface tailored to legal workflows.",
    imgSrc: "static/images/myp/1.webp",
    href: "https://myp.emirbaycan.com.tr"
  },
  {
    title: "Hukuki Yeterlilik Akademisi",
    description: "Comprehensive website and admin panel for an education services firm, built with Kalenuxer. Features secure course management, multi-level user access, and real-time updates, designed for scalability and seamless content delivery.",
    imgSrc: "static/images/hya/1.webp",
    href: "https://hya.emirbaycan.com.tr"
  },
  {
    title: "Morkoç Law Firm",
    description: "High-impact website and bespoke control panel for a law firm, built on Kalenuxer. Focus on speed, secure case management, and dynamic content delivery—tailored for the legal industry’s demanding standards.",
    imgSrc: "static/images/morkoc/1.webp",
    href: "https://lawnux.emirbaycan.com.tr"
  },
  {
    title: "Karalar Prefabric",
    description: "Fully-managed website and administration panel for a prefabricated housing firm, powered by Kalenuxer. Delivers advanced catalog management, customer interaction tools, and robust backend capabilities for business growth.",
    imgSrc: "static/images/kp/1.webp",
    href: "https://kp.emirbaycan.com.tr"
  },
  {
    title: "Eyüp Sultan Tulumbacısı",
    description: "Brand-forward website for a popular dessert company, developed with Kalenuxer. Optimized for user engagement and high-conversion, featuring product showcases and an intuitive, easy-to-manage backend.",
    imgSrc: "static/images/est/1.webp",
    href: "https://eyp.emirbaycan.com.tr"
  },
  {
    title: "Girişimci Hukukçular Derneği",
    description: "First-of-its-kind web platform and management system for a law society, utilizing the LAMP stack. Includes member management, event automation, and secure communications modules.",
    imgSrc: "static/images/ghd/1.webp",
    href: "https://ghd.emirbaycan.com.tr"
  },
  {
    title: "Hukuk Eğitim Programları",
    description: "End-to-end website and control panel for an education collective, continuously updated with new features. Built on Kalenuxer, supporting multi-course content and custom reporting.",
    imgSrc: "static/images/hep/1.webp",
    href: "https://hep.emirbaycan.com.tr"
  },
  {
    title: "Do Eloboost",
    description: "Robust website and backend system for an online gaming service, built with Kalenuxer and optimized for performance, automation, and secure client management.",
    imgSrc: "static/images/de/1.webp",
    href: "https://de.emirbaycan.com.tr"
  },
  {
    title: "Terapi Kliniği",
    description: "Dynamic website and control panel for a psychologist practice, engineered with Laravel and custom JavaScript libraries. Successfully adapted Laravel for standard shared hosting, optimizing both backend logic and client-side interactivity.",
    imgSrc: "static/images/tk/1.webp",
    href: ""
  },
  {
    title: "Murat Bulat Law Firm",
    description: "Feature-rich website and management panel for a law office, developed on the LAMP stack. Provides automated case management, secure client portals, and streamlined admin tools.",
    imgSrc: "static/images/mb/1.webp",
    href: ""
  },
  {
    title: "Portfolio w Kalenuxer",
    description: "Multi-language portfolio websites developed as a technical showcase using Kalenuxer and LAMP—demonstrating full-stack proficiency and clean, scalable architecture.",
    imgSrc: "static/images/lamp/1.webp",
    href: "https://lamp.emirbaycan.com.tr"
  },
  {
    title: "Portfolio w React",
    description: "Multi-language portfolio sites designed with React, Node.js, and MySQL on Ubuntu/Apache. Highlights advanced front-end techniques and seamless integration with backend infrastructure.",
    imgSrc: "static/images/mern/1.webp",
    href: "https://mern.emirbaycan.com.tr"
  },
  {
    title: "Portfolio w Laravel & React",
    description: "Full-stack portfolio websites built as technical proof-of-concept projects, combining Laravel, React, Node.js, and Three.js for modern, interactive UI/UX.",
    imgSrc: "static/images/nmlr/1.webp",
    href: "https://nmlr.emirbaycan.com.tr"
  },
  {
    title: "Portfolio w Nextjs",
    description: "Next.js-based multi-language portfolio sites, featuring dynamic content delivery, email integration via Resend, and scalable cloud hosting solutions.",
    imgSrc: "static/images/next/1.webp",
    href: "https://next.emirbaycan.com.tr"
  },
  {
    title: "Account Creator",
    description: "Automated account creator for social platforms, utilizing C#, Selenium, Geckofx, and cloud services (AWS, Google Cloud, Azure). Enables high-volume, unattended account registrations with VPN/proxy support.",
    imgSrc: "static/images/ac/1.webp",
    href: ""
  },
  {
    title: "Voter",
    description: "Automated human-data generator using Python, Selenium, and Tor Browser IP rotation—built for scalable, anonymized user simulation.",
    imgSrc: "static/images/v/1.webp",
    href: ""
  },
  {
    title: "Height and Speed Calculator",
    description: "Python-based algorithm to precisely calculate object height from input parameters—demonstrating applied math and algorithmic thinking.",
    imgSrc: "static/images/shc/1.webp",
    href: ""
  },
  {
    title: "Digital Screen Detector",
    description: "Real-time detection of digital screens from live camera feeds, leveraging Python and YOLO for computer vision applications. [GitHub](https://github.com/emirbaycan/yolo_digital_screen_detector)",
    imgSrc: "static/images/dsd/1.webp",
    href: "https://github.com/emirbaycan/yolo_digital_screen_detector"
  },
  {
    title: "Digital Screen Reader",
    description: "Automated detection and reading of digital screens in live video streams, integrating OCR and computer vision with Python. [GitHub](https://github.com/emirbaycan/ocr_digital_screen_reader)",
    imgSrc: "static/images/dsr/1.webp",
    href: "https://github.com/emirbaycan/ocr_digital_screen_reader"
  },
  {
    title: "Digital Screen Alarm",
    description: "Real-time digital screen monitoring with image capture and threshold-based alerting—triggers image saves when values exceed specified limits. [GitHub](https://github.com/emirbaycan/digital_screen_alarm_with_rtsp_camera)",
    imgSrc: "static/images/dsa/1.webp",
    href: "https://github.com/emirbaycan/digital_screen_alarm_with_rtsp_camera"
  }
]



export default projectsData
