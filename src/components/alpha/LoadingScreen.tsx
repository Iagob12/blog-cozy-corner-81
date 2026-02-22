import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { TrendingUp } from "lucide-react";

const loadingSteps = [
	"Carregando CSV com 200+ ações",
	"Radar de Oportunidades",
	"Triagem Fundamentalista",
	"Buscando Releases",
	"Preços em tempo real",
	"Análise Profunda",
	"Verificação Anti-Manada",
	"Gerando ranking",
];

export default function LoadingScreen() {
	const [currentStep, setCurrentStep] = useState(0);
	const [progress, setProgress] = useState(0);

	useEffect(() => {
		const totalSteps = loadingSteps.length;
		const stepDuration = 8000; // 8 segundos por step
		
		let currentStepIndex = 0;
		let stepProgress = 0;

		const interval = setInterval(() => {
			stepProgress += 1;
			
			if (stepProgress >= 100) {
				stepProgress = 0;
				currentStepIndex = Math.min(currentStepIndex + 1, totalSteps - 1);
				setCurrentStep(currentStepIndex);
			}

			const totalProgress = ((currentStepIndex * 100 + stepProgress) / (totalSteps * 100)) * 100;
			setProgress(Math.min(totalProgress, 99));
		}, stepDuration / 100);

		return () => clearInterval(interval);
	}, []);

	return (
		<div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20 flex items-center justify-center p-4">
			<motion.div
				initial={{ opacity: 0, y: 20 }}
				animate={{ opacity: 1, y: 0 }}
				className="w-full max-w-md"
			>
				{/* Logo */}
				<motion.div
					className="text-center mb-12"
					initial={{ scale: 0.9, opacity: 0 }}
					animate={{ scale: 1, opacity: 1 }}
					transition={{ delay: 0.1 }}
				>
					<div className="inline-flex items-center gap-3">
						<div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center">
							<TrendingUp className="w-6 h-6 text-primary-foreground" />
						</div>
						<h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
							Alpha Terminal
						</h1>
					</div>
				</motion.div>

				{/* Progress */}
				<motion.div
					initial={{ opacity: 0 }}
					animate={{ opacity: 1 }}
					transition={{ delay: 0.3 }}
				>
					{/* Status Text */}
					<div className="text-center mb-4">
						<p className="text-sm text-muted-foreground font-medium">
							{loadingSteps[currentStep]}
						</p>
					</div>

					{/* Progress Bar */}
					<div className="relative">
						<div className="h-1.5 bg-muted/50 rounded-full overflow-hidden backdrop-blur-sm">
							<motion.div
								className="h-full bg-gradient-to-r from-primary via-primary/80 to-primary rounded-full"
								initial={{ width: 0 }}
								animate={{ width: `${progress}%` }}
								transition={{ duration: 0.3, ease: "easeOut" }}
							/>
						</div>
						
						{/* Percentage */}
						<div className="flex justify-center mt-3">
							<span className="text-xs font-mono text-muted-foreground">
								{Math.round(progress)}%
							</span>
						</div>
					</div>
				</motion.div>
			</motion.div>
		</div>
	);
}
